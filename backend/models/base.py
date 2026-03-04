"""Base model class with common fields and functionality."""
from datetime import datetime
from extensions import db


class BaseModel(db.Model):
    """Abstract base model with common fields for all models.
    
    Provides:
    - Primary key (id)
    - Timestamp fields (created_at, updated_at)
    - Automatic timestamp management
    - Common query methods
    """
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def save(self):
        """Save the model instance to the database.
        
        Returns:
            self: The saved model instance
        """
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model instance from the database."""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """Update model attributes and save to database.
        
        Args:
            **kwargs: Attribute names and values to update
            
        Returns:
            self: The updated model instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def to_dict(self):
        """Convert model instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the model
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Convert datetime objects to ISO format strings
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    @classmethod
    def find_by_id(cls, id):
        """Find a model instance by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        return cls.query.get(id)
    
    @classmethod
    def find_all(cls):
        """Find all instances of the model.
        
        Returns:
            list: List of all model instances
        """
        return cls.query.all()
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__} {self.id}>"
