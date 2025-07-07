from app import db
from flask_login import UserMixin

class User_details(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    snippets = db.relationship("Snippet", backref="user")

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    language = db.Column(db.String(50))
    explanation = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20))
    test_case = db.Column(db.Text)
