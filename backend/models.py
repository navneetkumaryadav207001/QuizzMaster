from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    scores = db.relationship('Scores', backref='user', lazy=True, cascade="all, delete-orphan")  # Backref added

class Subjects(db.Model):  
    __tablename__ = 'subjects'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    chapters = db.relationship('Chapters', backref='subject', lazy=True, cascade="all, delete-orphan") 

class Chapters(db.Model):  
    __tablename__ = 'chapters'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Changed title -> name for consistency
    description = db.Column(db.String(255), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # In minutes
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Scores', backref='quiz', lazy=True, cascade="all, delete-orphan")  # Backref added

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)  # Fixed ForeignKey reference
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'

# ✅ New Scores Model
class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)  # Link to Quiz
    score = db.Column(db.Integer, nullable=False)  # User's score
    total_questions = db.Column(db.Integer, nullable=False)  # Total number of questions
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when quiz was attempted
