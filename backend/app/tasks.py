from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.models import User, Question
from config import Config
import random

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def send_daily_questions():
    users = User.query.all()
    for user in users:
        questions = Question.query.join(Document).filter(Document.user_id == user.id).order_by(func.random()).limit(5).all()
        if questions:
            question_text = "\n".join([f"{i+1}. {q.content}" for i, q in enumerate(questions)])
            message = Mail(
                from_email='quiz@yourdomain.com',
                to_emails=user.email,
                subject='Your Daily Quiz Questions',
                html_content=f'<p>Here are your daily quiz questions:</p><pre>{question_text}</pre>'
            )
            try:
                sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
                response = sg.send(message)
            except Exception as e:
                print(str(e))

# Schedule this task to run daily at 8:00 AM
