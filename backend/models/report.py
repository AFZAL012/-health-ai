"""Report model for storing generated diagnostic reports."""
import uuid
from extensions import db
from models.base import BaseModel


class Report(BaseModel):
    """Report model for generated diagnostic reports.
    
    Stores metadata and file information for PDF/HTML reports generated
    from symptom analyses.
    """
    
    __tablename__ = 'reports'
    
    report_id = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    analysis_id = db.Column(
        db.Integer,
        db.ForeignKey('analyses.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    format = db.Column(db.String(10), default='pdf', nullable=False)
    file_path = db.Column(db.String(500), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    analysis = db.relationship('Analysis', back_populates='reports')
    
    def to_dict(self):
        """Convert report to dictionary.
        
        Returns:
            dict: Report data with all fields
        """
        result = super().to_dict()
        return result
    
    def __repr__(self):
        """String representation of Report."""
        return f"<Report {self.report_id}: {self.format}>"
