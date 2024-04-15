from extensions import db
import uuid
from flask_login import UserMixin


class ContactUs(UserMixin, db.Model):
    __tablename__ = "ContactUs"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    message = db.Column(db.String(500))
    created_at = db.Column(db.Date)
    status = db.Column(db.Boolean)


def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "phone_number": self.phone_number,
        "message": self.message,
        "created_date": self.created_date,
        "status": self.status,
    }
