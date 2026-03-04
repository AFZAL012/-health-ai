"""Symptom model for symptom dictionary and NLP processing."""
from extensions import db
from models.base import BaseModel


class Symptom(BaseModel):
    """Symptom model storing canonical symptom names and synonyms.
    
    Stores symptom information including canonical names, categories,
    synonyms for NLP matching, and related symptoms for suggestions.
    Supports full-text search for efficient symptom lookup.
    """
    
    __tablename__ = 'symptoms'
    
    canonical_name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100))
    synonyms = db.Column(db.JSON)
    related_symptoms = db.Column(db.JSON)
    
    # Full-text search index for PostgreSQL
    # Note: This will be created in the migration file
    __table_args__ = (
        db.Index('idx_symptom_search', 'canonical_name', postgresql_using='gin', postgresql_ops={'canonical_name': 'gin_trgm_ops'}),
    )
    
    def __repr__(self):
        """String representation of Symptom."""
        return f"<Symptom {self.id}: {self.canonical_name}>"
