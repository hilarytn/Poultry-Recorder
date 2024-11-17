from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import uuid

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(512), nullable=True)
    feeds = db.relationship("Feed", back_populates="user")

    def to_dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'