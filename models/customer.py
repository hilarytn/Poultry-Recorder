from extensions import db
import uuid

class Customer(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='customers')

    def __repr__(self):
        return f"<Customer {self.name}>"
