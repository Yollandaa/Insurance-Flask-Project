from extensions import db
import uuid
from flask_login import UserMixin


class Vehicle(UserMixin, db.Model):
    __tablename__ = "Vehicle"

    vehicle_id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(50), db.ForeignKey("Users.id"))
    car_type = db.Column(db.String(50))
    year = db.Column(db.Integer)
    num_accidents = db.Column(db.Integer)

    user = db.relationship("User", back_populates="vehicles")
    policy = db.relationship("Policy", back_populates="vehicle")

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id,
            "car_type": self.car_type,
            "year": self.year,
            "num_accidents": self.num_accidents,
        }
