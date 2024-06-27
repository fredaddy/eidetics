from google.cloud import storage
import openai
from app import db
from app.models import Question
from config import Config

def upload_file_to_gcs(file):
    client = storage.Client(project=Config.GOOGLE_CLOUD_PROJECT)
    bucket = client.bucket(Config.GOOGLE_CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    return blob.public_url

def generate_questions(document_id, gcs_url):
    # Download the file from GCS and extract text
    # For simplicity, let's assume we have the text content
    text_content = "Sample text content from the document"
    
    openai.api_key = Config.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Generate 5 quiz questions based on the following text:\n\n{text_content}\n\nQuestions:",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    questions = response.choices[0].text.strip().split('\n')
    
    for question in questions:
        new_question = Question(content=question, document_id=document_id)
        db.session.add(new_question)
    
    db.session.commit()
