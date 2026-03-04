"""DiseaseTranslation model for multi-language support."""
from extensions import db
from models.base import BaseModel


class DiseaseTranslation(BaseModel):
    """DiseaseTranslation model for multi-language disease information.
    
    Stores translated disease information including name, description,
    and precautions in different languages. Linked to Disease model
    via foreign key relationship.
    """
    
    __tablename__ = 'disease_translations'
    
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), nullable=False, index=True)
    language_code = db.Column(db.String(10), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    precautions = db.Column(db.JSON)
    
    # Relationships
    disease = db.relationship('Disease', back_populates='translations')
    
    # Ensure unique combination of disease and language
    __table_args__ = (
        db.UniqueConstraint('disease_id', 'language_code', name='uq_disease_language'),
    )
    
    def __repr__(self):
        """String representation of DiseaseTranslation."""
        return f"<DiseaseTranslation {self.id}: Disease {self.disease_id} ({self.language_code})>"
