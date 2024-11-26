from extensions import db
from datetime import datetime, timezone
import uuid

class Vaccination(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vaccine_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)
    batch_id = db.Column(db.String(36), db.ForeignKey('batch.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    batch = db.relationship('Batch', back_populates='vaccinations')
    user = db.relationship('User', back_populates='vaccinations')

    def __repr__(self):
        return f'<Vaccination {self.vaccine_name}>'