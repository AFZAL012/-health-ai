"""Analysis model for storing symptom analyses and predictions."""
import uuid
from extensions import db
from models.base import BaseModel


class Analysis(BaseModel):
    """Analysis model for symptom analysis results.
    
    Stores symptom data, disease predictions, risk assessments, and recommendations
    for both authenticated and anonymous users.
    """
    
    __tablename__ = 'analyses'
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    analysis_id = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    symptoms = db.Column(db.JSON, nullable=False)
    predictions = db.Column(db.JSON, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    recommendations = db.Column(db.JSON, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='analyses')
    reports = db.relationship(
        'Report',
        back_populates='analysis',
        cascade='all, delete-orphan'
    )
    
    # Indexes for query optimization
    __table_args__ = (
        db.Index('idx_user_created', 'user_id', 'created_at'),
    )
    
    def to_dict(self):
        """Convert analysis to dictionary.
        
        Returns:
            dict: Analysis data with all fields
        """
        result = super().to_dict()
        # Ensure JSON fields are properly serialized
        if result.get('symptoms') is None:
            result['symptoms'] = []
        if result.get('predictions') is None:
            result['predictions'] = []
        if result.get('recommendations') is None:
            result['recommendations'] = []
        return result
    
    def __repr__(self):
        """String representation of Analysis."""
        return f"<Analysis {self.analysis_id}: Risk {self.risk_level}>"
