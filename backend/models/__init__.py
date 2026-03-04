"""Database models package."""
from extensions import db
from models.base import BaseModel
from models.user import User
from models.user_profile import UserProfile
from models.analysis import Analysis
from models.report import Report
from models.disease import Disease
from models.symptom import Symptom
from models.disease_translation import DiseaseTranslation

# Import models here for easy access
# Models will be imported as they are created in subsequent tasks

__all__ = [
    'db',
    'BaseModel',
    'User',
    'UserProfile',
    'Analysis',
    'Report',
    'Disease',
    'Symptom',
    'DiseaseTranslation'
]
