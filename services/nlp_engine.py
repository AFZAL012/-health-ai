import spacy
import re

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens)

def detect_duration(text):
    match = re.search(r"\d+\s*(day|week|month|year)s?", text.lower())
    return match.group() if match else None

def detect_severity(text):
    severity_words = ["mild", "severe", "intense", "chronic", "unbearable"]
    for word in severity_words:
        if word in text.lower():
            return word
    return "normal"

def detect_emergency(text):
    emergency_words = ["chest pain", "breathing difficulty", "stroke", "unconscious"]
    for word in emergency_words:
        if word in text.lower():
            return True
    return False