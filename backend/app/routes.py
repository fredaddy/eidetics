from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Document
from app.utils import upload_file_to_gcs, generate_questions

bp = Blueprint('main', __name__)

@bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        gcs_url = upload_file_to_gcs(file)
        document = Document(filename=file.filename, user_id=user_id)
        db.session.add(document)
        db.session.commit()
        
        generate_questions.delay(document.id, gcs_url)
        
        return jsonify({'message': 'File uploaded successfully', 'document_id': document.id}), 200

# Add more routes as needed
