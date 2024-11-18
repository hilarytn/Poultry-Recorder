from extensions import db
from datetime import datetime, timezone
import uuid

class Batch(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    end_date = db.Column(db.DateTime, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="active")
    mortality = db.Column(db.Integer, nullable=False)
    feed_id = db.Column(db.String(36), db.ForeignKey('feed.id'), nullable=True)
    feed = db.relationship('Feed', back_populates='batches')
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='batches')
    
    def __repr__(self):
        return f'<Batch {self.name}>'