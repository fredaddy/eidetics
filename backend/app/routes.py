from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models import Document
from app.utils import upload_file_to_gcs, generate_questions

bp = Blueprint('main', __name__)

@bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        filename = secure_filename(file.filename)
        gcs_url = upload_file_to_gcs(file)
        document = Document(filename=filename, user_id=None)  # Set user_id to None explicitly if not provided
        db.session.add(document)
        db.session.commit()
        
        generate_questions.delay(document.id, gcs_url)
        
        return jsonify({'message': 'File uploaded successfully', 'document_id': document.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500