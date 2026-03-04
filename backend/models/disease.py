"""Disease model for medical knowledge database."""
from extensions import db
from models.base import BaseModel


class Disease(BaseModel):
    """Disease model storing comprehensive disease information.
    
    Stores disease details including description, severity, symptoms,
    specialist recommendations, precautions, and lifestyle recommendations.
    Supports multi-language translations through DiseaseTranslation model.
    """
    
    __tablename__ = 'diseases'
    
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    common_symptoms = db.Column(db.JSON)
    specialist = db.Column(db.String(100))
    precautions = db.Column(db.JSON)
    lifestyle_recommendations = db.Column(db.JSON)
    urgency_guidelines = db.Column(db.Text)
    
    # Relationships
    translations = db.relationship(
        'DiseaseTranslation',
        back_populates='disease',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        """String representation of Disease."""
        return f"<Disease {self.id}: {self.name}>"
