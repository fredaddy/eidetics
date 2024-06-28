from google.cloud import storage
import openai
from app import db
from app.models import Question
from config import Config
import logging

def upload_file_to_gcs(file):
    from google.cloud import storage
    import os

    client = storage.Client()
    bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
    
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        logging.info("Upload successful: {}".format(blob.public_url))
        return blob.public_url
    except Exception as e:
        logging.error("Failed to upload to GCS: {}".format(str(e)))
        raise

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
