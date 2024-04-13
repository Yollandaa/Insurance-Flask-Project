from extensions import db
import uuid
from flask_login import UserMixin


# Task - User Model | id, username, password
# Sign Up page
# Login page
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.Integer, nullable=False, unique=True)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    license_year_issue = db.Column(db.DATE)

    # Define relationship to Policy
    vehicles = db.relationship("Vehicle", back_populates="user")
    policies = db.relationship("Policy", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "id_number": self.id_number,
            "phone_number": self.phone_number,
            "email": self.email,
            "license_year_issue": self.license_year_issue,
        }
