from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.subjects import manage_subjects
from routes.chapters import manage_chapters
from routes.quizzes import manage_quizzes
from routes.questions import manage_questions
from routes.register import register
from routes.login import login
from routes.allchapters import get_all_chapters
from routes.scores import get_user_scores, submit_score
from flask_mail import Mail ,Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "supersecretkey"
app.config["JWT_HEADER_TYPE"] = "JWT"

CORS(app)
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all() 

# Yandex SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp.yandex.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'yadavnavneet@yandex.com'
app.config['MAIL_PASSWORD'] = 'ntqfvgvjfyoapxkw'
app.config['MAIL_DEFAULT_SENDER'] = 'yadavnavneet@yandex.com'
mail = Mail(app)

# Celery Configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Subjects & Chapters
app.add_url_rule("/subjects", "subjects", manage_subjects, methods=["GET", "POST","DELETE","PUT"])
app.add_url_rule("/subjects/<int:subject_id>/chapters", "chapters", manage_chapters, methods=["GET", "POST", "DELETE","PUT"])

# Quizzes & Questions
app.add_url_rule("/Quizzs", "quizzes", manage_quizzes, methods=["GET", "POST", "DELETE"])
app.add_url_rule("/questions", "questions", manage_questions, methods=["GET", "POST", "DELETE"])
app.add_url_rule("/chapters","allchapters",get_all_chapters,methods=["GET"])
app.add_url_rule('/scores',"getScores", get_user_scores, methods=['GET'])
app.add_url_rule('/scores',"postScores",submit_score, methods=['POST'])

# Authentication
app.add_url_rule("/register", "register", register, methods=["POST"])
app.add_url_rule("/login", "login", login, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
