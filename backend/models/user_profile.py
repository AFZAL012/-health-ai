"""UserProfile model for user demographics and preferences."""
from extensions import db
from models.base import BaseModel


class UserProfile(BaseModel):
    """User profile model for demographics and preferences.
    
    Stores user-specific information including medical history,
    emergency contacts, and application preferences.
    """
    
    __tablename__ = 'user_profiles'
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    medical_history = db.Column(db.JSON, nullable=True, default=list)
    emergency_contact = db.Column(db.JSON, nullable=True, default=dict)
    language_preference = db.Column(db.String(10), default='en', nullable=False)
    theme_preference = db.Column(db.String(10), default='light', nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='profile')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('age > 0 AND age < 150', name='valid_age'),
    )
    
    def to_dict(self):
        """Convert profile to dictionary.
        
        Returns:
            dict: Profile data
        """
        result = super().to_dict()
        # Ensure JSON fields are properly serialized
        if result.get('medical_history') is None:
            result['medical_history'] = []
        if result.get('emergency_contact') is None:
            result['emergency_contact'] = {}
        return result
    
    def __repr__(self):
        """String representation of UserProfile."""
        return f"<UserProfile {self.id}: User {self.user_id}>"
