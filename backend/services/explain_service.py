import os
import joblib
import pandas as pd
import numpy as np
import shap

class ExplainService:
    _explainer = None
    _model = None
    _symptom_columns = None

    @classmethod
    def _initialize(cls):
        if cls._explainer is not None:
            return

        MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_models', 'model.pkl')
        SYMPTOMS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_models', 'symptom_columns.pkl')

        try:
            cls._model = joblib.load(MODEL_PATH)
            cls._symptom_columns = joblib.load(SYMPTOMS_PATH)

            # For tree-based models (like RandomForest), TreeExplainer is efficient
            # If the model is from scikit-learn, we can genericize or use KernelExplainer
            cls._explainer = shap.TreeExplainer(cls._model)
        except Exception as e:
            print(f"Error initializing SHAP explainer: {e}")

    @classmethod
    def explain_prediction(cls, input_data):
        """
        Generates SHAP values for a given prediction.

        Args:
            input_data (list): Binary list representing matched symptoms.

        Returns:
            dict: Contribution of each symptom to the prediction.
        """
        cls._initialize()
        if cls._explainer is None:
            return {}

        try:
            input_df = pd.DataFrame([input_data], columns=cls._symptom_columns)
            shap_values = cls._explainer.shap_values(input_df)

            # Map symptom names to their SHAP values
            explanations = []

            # Identify the predicted class index
            probabilities = cls._model.predict_proba(input_df)[0]
            predicted_class_index = np.argmax(probabilities)

            # Handle different SHAP output formats (list vs array)
            if isinstance(shap_values, list):
                # Multi-class output: list of arrays (one per class)
                # Ensure index is within bounds
                if predicted_class_index < len(shap_values):
                    class_shap_values = shap_values[predicted_class_index]
                else:
                    class_shap_values = shap_values[-1] # Fallback

                # If it's still a 2D array (samples, features), take first sample
                if len(class_shap_values.shape) > 1:
                    class_shap_values = class_shap_values[0]
            elif isinstance(shap_values, np.ndarray):
                # Array output: check dimensions
                if len(shap_values.shape) == 3: # (classes, samples, features)
                    if predicted_class_index < shap_values.shape[0]:
                        class_shap_values = shap_values[predicted_class_index][0]
                    else:
                        class_shap_values = shap_values[-1][0]
                elif len(shap_values.shape) == 2: # (samples, features)
                    class_shap_values = shap_values[0]
                else:
                    class_shap_values = shap_values
            else:
                raise ValueError(f"Unexpected SHAP values type: {type(shap_values)}")

            for i, val in enumerate(class_shap_values):
                if input_data[i] == 1: # Only include symptoms that were present
                    explanations.append({
                        "symptom": cls._symptom_columns[i].replace("_", " "),
                        "impact": float(val)
                    })

            # Sort by impact (descending)
            explanations.sort(key=lambda x: x["impact"], reverse=True)

            return {
                "predicted_class": cls._model.classes_[predicted_class_index],
                "contributions": explanations[:5] # Top 5 contributors
            }
        except Exception as e:
            print(f"DEBUG: SHAP computation error: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
