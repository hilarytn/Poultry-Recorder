from extensions import db
from datetime import datetime, timezone
import uuid

class Expense(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    date_incurred = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    batch_id = db.Column(db.String(36), db.ForeignKey('batch.id'), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    batch = db.relationship('Batch', back_populates='expenses') 
    user = db.relationship('User', back_populates='expenses')

    def __repr__(self):
        return f'<Expense {self.title} - {self.amount}>'
