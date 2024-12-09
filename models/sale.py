from extensions import db
from datetime import datetime, timezone
import uuid

class Sale(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    batch_id = db.Column(db.String(36), db.ForeignKey('batch.id'), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False) 
    batch = db.relationship('Batch', back_populates='sales')
    user = db.relationship('User', back_populates='sales')

    def __repr__(self):
        return f'<Sale {self.item} - {self.total_amount}>'