# src/routes/uploads.py

from flask import Blueprint, request, jsonify
import os
from src.configs.configs import UPLOAD_FOLDER

upload_svg_bp = Blueprint('upload_svg', __name__)

ALLOWED_EXTENSIONS = {'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_svg_bp.route('/upload_svg', methods=['POST'])
def upload_svg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)
        print(f"Saving SVG: {file.filename} -> {save_path}")
        return jsonify({'status': 'success', 'path': f'/static/images/{file.filename}'})
    else:
        return jsonify({'error': 'Invalid file type'}), 400
