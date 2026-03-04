import os
import joblib
import pandas as pd
import numpy as np
import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.rbac import require_role
from models.analysis import Analysis
from extensions import db, limiter
from services.explain_service import ExplainService

predict_bp = Blueprint('predict', __name__)

# ===============================
# Load Model & Symptom Columns
# ===============================
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_models', 'model.pkl')
SYMPTOMS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_models', 'symptom_columns.pkl')

try:
    model = joblib.load(MODEL_PATH)
    symptom_columns = joblib.load(SYMPTOMS_PATH)
    formatted_symptoms = [s.replace("_", " ") for s in symptom_columns]
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    symptom_columns = []
    formatted_symptoms = []

# ===============================
# Symptom Synonyms
# ===============================
SYMPTOM_SYNONYMS = {
    "rash": "skin rash",
    "rashes": "skin rash",
    "red rash": "skin rash",
    "red rashes": "skin rash",
    "skin redness": "skin rash",
    "redness": "skin rash",
    "high temperature": "fever",
    "body heat": "fever",
    "vomit": "vomiting"
}

# ===============================
# Doctor Specialization Mapping
# ===============================
DOCTOR_SPECIALIZATION = {
    "Fungal infection": "Dermatologist",
    "Allergy": "Dermatologist",
    "Acne": "Dermatologist",
    "Heart attack": "Cardiologist",
    "Hypertension": "Cardiologist",
    "Migraine": "Neurologist",
    "Paralysis (brain hemorrhage)": "Neurologist",
    "Diabetes": "Endocrinologist",
    "Hypothyroidism": "Endocrinologist",
    "Hyperthyroidism": "Endocrinologist",
    "Pneumonia": "Pulmonologist",
    "Bronchial Asthma": "Pulmonologist",
    "Arthritis": "Orthopedic",
    "Osteoarthristis": "Orthopedic",
    "Tuberculosis": "Pulmonologist",
    "GERD": "Gastroenterologist",
    "Peptic ulcer diseae": "Gastroenterologist",
}

def normalize_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.lower().split()
    words = [w[:-1] if w.endswith('s') else w for w in words]
    return " ".join(words)

def calculate_risk(probability):
    if probability >= 75:
        return "High"
    elif probability >= 40:
        return "Medium"
    else:
        return "Low"

def match_symptoms(user_input):
    if not symptom_columns:
        return [], []

    input_data = [0] * len(symptom_columns)
    matched_symptoms = []
    user_input = user_input.lower()

    # Apply synonym replacement
    for key, value in SYMPTOM_SYNONYMS.items():
        if key in user_input:
            user_input = user_input.replace(key, value)

    user_input = normalize_text(user_input)

    for i, symptom in enumerate(formatted_symptoms):
        normalized_symptom = normalize_text(symptom)
        if normalized_symptom in user_input:
            input_data[i] = 1
            matched_symptoms.append(symptom)

    return input_data, matched_symptoms

@predict_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_symptoms():
    if not model or not symptom_columns:
        return jsonify({"error": "Model not loaded properly"}), 500

    data = request.json
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Missing 'symptoms' in request body"}), 400

    user_input = data['symptoms'].strip()
    input_data, matched_symptoms = match_symptoms(user_input)
    print(f"DEBUG: Input symptoms: {user_input}, Matched: {matched_symptoms}")

    if sum(input_data) == 0:
        return jsonify({
            "prediction": "No matching symptoms found. Please provide more details.",
            "probability": 0,
            "risk": "Low",
            "top_diseases": [],
            "matched_symptoms": [],
            "doctor": "General Physician"
        }), 200

    input_df = pd.DataFrame([input_data], columns=symptom_columns)
    probabilities = model.predict_proba(input_df)[0]
    top_indices = np.argsort(probabilities)[-3:][::-1]

    top_diseases = [
        {"disease": model.classes_[i], "probability": round(probabilities[i] * 100, 2)}
        for i in top_indices
    ]

    prediction = top_diseases[0]["disease"]
    probability = top_diseases[0]["probability"]
    risk_level = calculate_risk(probability)
    doctor = DOCTOR_SPECIALIZATION.get(prediction, "General Physician")

    # Generate SHAP explanation
    try:
        explanation = ExplainService.explain_prediction(input_data)
    except Exception as e:
        print(f"DEBUG: ExplainService failed: {e}")
        explanation = {"error": str(e)}

    # Save to database if user is authenticated
    current_user_id = get_jwt_identity()
    analysis_id = None

    if current_user_id:
        try:
            # Cast back to int for database foreign key (which is Integer)
            user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
            new_analysis = Analysis(
                user_id=user_id,
                symptoms={"input": user_input, "matched": matched_symptoms},
                predictions=top_diseases,
                risk_level=risk_level,
                recommendations={
                    "doctor": doctor,
                    "precautions": [],
                    "explanation": explanation
                },
                notes=None
            )
            db.session.add(new_analysis)
            db.session.commit()
            analysis_id = new_analysis.analysis_id
        except Exception as e:
            db.session.rollback()
            print(f"Error saving analysis: {e}")

    return jsonify({
        "analysis_id": analysis_id,
        "prediction": prediction,
        "probability": probability,
        "risk": risk_level,
        "top_diseases": top_diseases,
        "matched_symptoms": matched_symptoms,
        "doctor": doctor,
        "explanation": explanation
    }), 200
@predict_bp.route('/history', methods=['GET'])
@limiter.exempt
@jwt_required()
def get_history():
    current_user_id = get_jwt_identity()
    analyses = Analysis.query.filter_by(user_id=current_user_id).order_by(Analysis.created_at.desc()).all()

    history = []
    for a in analyses:
        history.append({
            "analysis_id": a.analysis_id,
            "prediction": a.predictions[0]["disease"] if a.predictions else "Unknown",
            "risk": a.risk_level,
            "created_at": a.created_at.isoformat(),
            "top_diseases": a.predictions,
            "matched_symptoms": a.symptoms.get("matched", []),
            "doctor": a.recommendations.get("doctor", "General Physician")
        })

    return jsonify({"history": history}), 200

@predict_bp.route('/analysis/<id>', methods=['GET'])
@jwt_required()
def get_analysis_details(id):
    current_user_id = get_jwt_identity()
    analysis = Analysis.query.filter_by(analysis_id=id, user_id=current_user_id).first()

    if not analysis:
        return jsonify({"error": "Analysis not found"}), 404

    return jsonify({
        "analysis_id": analysis.analysis_id,
        "prediction": analysis.predictions[0]["disease"] if analysis.predictions else "Unknown",
        "probability": analysis.predictions[0]["probability"] if analysis.predictions else 0,
        "risk": analysis.risk_level,
        "top_diseases": analysis.predictions,
        "matched_symptoms": analysis.symptoms.get("matched", []),
        "doctor": analysis.recommendations.get("doctor", "General Physician"),
        "created_at": analysis.created_at.isoformat()
    }), 200
