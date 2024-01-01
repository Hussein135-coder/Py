import os
from docx import Document
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_files(request):
    uploaded_files = request.files.getlist('files')
    file_paths = []
    # Temporary directory to store user-uploaded files
    temp_directory = UPLOAD_FOLDER
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_directory, filename)
            file.save(file_path)
            file_paths.append(file_path)
    return file_paths


def convert_to_docx(file_paths):
    converted_paths = []
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                print(f"Converting file: {file_path}")
                doc = Document(file_path)
                docx_filename = os.path.splitext(os.path.basename(file_path))[0] + '.docx'
                docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
                doc.save(docx_path)
                converted_paths.append(docx_path)
                print(f"Converted file path: {docx_path}")
            else:
                print(f"File not found at '{file_path}'")
        except Exception as e:
            print(f"Error converting file '{file_path}' to DOCX: {e}")
    return converted_paths
