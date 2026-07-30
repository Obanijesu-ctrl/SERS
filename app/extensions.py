"""
Shared extension instances.
Kept in their own module to avoid circular imports between
app/__init__.py and the model / route modules.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
