from extensions import db
import uuid
from flask_login import UserMixin


class Claims(UserMixin, db.Model):
    __tablename__ = "Claims"

    claim_id = db.Column(db.String(50), primary_key=True)
    policy_id = db.Column(db.String(50), db.ForeignKey("Policy.policy_id"))
    date_filed = db.Column(db.Date)
    description = db.Column(db.String(500))
    status = db.Column(db.String(50))

    # Define relationship with Policy
    policy = db.relationship("Policy", back_populates="claims")

    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "policy_id": self.policy_id,
            "date_filed": self.date_filed,
            "description": self.description,
            "status": self.status,
        }
