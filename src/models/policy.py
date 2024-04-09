from extensions import db
import uuid
from flask_login import UserMixin
from models.claims import Claims
from models.vehicle import Vehicle


class Policy(db.Model):
    __tablename__ = "Policy"

    policy_id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(50), db.ForeignKey("Users.id"))
    vehicle_id = db.Column(db.String(50), db.ForeignKey("Vehicle.vehicle_id"))
    policy_type = db.Column(db.String(50))
    coverage_amount = db.Column(db.DECIMAL(10, 2))
    premium_amount = db.Column(db.DECIMAL(10, 2))
    start_date = db.Column(db.DATE)
    end_date = db.Column(db.DATE)
    status = db.Column(db.String(20))

    # Define relationships
    user = db.relationship("User", back_populates="policies")
    vehicle = db.relationship("Vehicle", back_populates="policy")
    claims = db.relationship("Claims", back_populates="policy")


def to_dict(self):
    return {
        "policy_id": self.policy_id,
        "user_id": self.user_id,
        "vehicle_id": self.vehicle_id,
        "policy_type": self.policy_type,
        "coverage_amount": self.coverage_amount,
        "premium_amount": self.premium_amount,
        "start_date": self.start_date,
        "end_date": self.end_date,
        "status": self.status,
    }
