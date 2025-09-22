from flask import Flask, flash, request, jsonify


ALLOWED_EXTENSIONS = {'ids'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file provided')
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']

        # check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # check if file has .ids extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .ids files are allowed'}), 400
        
    
        # get file data
        file_bytes = file.read()
        file_text = file_bytes.decode('utf-8')
        
        # return file data for further processing
        return jsonify({
            'filename': file.filename,
            'content_bytes': file_bytes.hex(),
            'content_text': file_text,
            'size': len(file_bytes),
            'mimetype': file.mimetype
        })

