from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    """
    A system user. Two roles are supported:
      - "admin"    : can manage communities and energy sources
      - "operator" : can view dashboards and toggle sources on/off
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="operator", nullable=False)
    is_active_account = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    # Flask-Login expects an `is_active` property distinct from our
    # `is_active_account` column name (avoids clashing with EnergySource.is_active).
    @property
    def is_active(self):
        return self.is_active_account

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
