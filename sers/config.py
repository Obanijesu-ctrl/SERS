"""
Central configuration. All environment-dependent values are read from
environment variables so the same codebase runs locally and in production
(e.g. Render, Railway) without code changes.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'sers.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
