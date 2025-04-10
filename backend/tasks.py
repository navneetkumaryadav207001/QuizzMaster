from datetime import datetime, timedelta
from flask_mail import Message
from app import app, db, mail
from celery_config import make_celery
from models import User, Quiz

celery = make_celery(app)

@celery.task
def send_daily_reminders():
    print("reminder sent")
    with app.app_context():
        users = User.query.all()

        for user in users:
                msg = Message("Test Email", recipients=[user.username])
                msg.body = f"Hi {user.username}, there's a new quiz for you! Visit now: QuizzMaster"
                mail.send(msg)
        return users

