from celery import Celery
from flask_mail import Message
from app import mail
from app.models import User, Question
import random

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def send_daily_questions():
    users = User.query.all()
    for user in users:
        questions = Question.query.join(Document).filter(Document.user_id == user.id).order_by(func.random()).limit(5).all()
        if questions:
            question_text = "\n".join([f"{i+1}. {q.content}" for i, q in enumerate(questions)])
            msg = Message('Your Daily Quiz Questions',
                          sender='your-email@gmail.com',
                          recipients=[user.email])
            msg.body = f'Here are your daily quiz questions:\n\n{question_text}'
            mail.send(msg)

# Schedule this task to run daily at 8:00 AM