from app import db
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User_details(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    preferences = db.Column(db.Text)  # Store as JSON string, e.g. {"theme": "dark", "fontSize": 14}
    snippets = db.relationship("Snippet", backref="user")

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    language = db.Column(db.String(50))
    explanation = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starter_code_python = db.Column(db.Text, nullable=False)
    starter_code_cpp = db.Column(db.Text, nullable=True)
    starter_code_java = db.Column(db.Text, nullable=True)
    starter_code_javascript = db.Column(db.Text, nullable=True)
    starter_code_csharp = db.Column(db.Text, nullable=True)
    test_cases = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(32), nullable=False)

class UserChallengeProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    attempts = db.Column(db.Integer, default=0)
    solved = db.Column(db.Boolean, default=False)
    last_code = db.Column(db.Text)
    last_feedback = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    challenge = db.relationship("Challenge", backref="progress_records")
