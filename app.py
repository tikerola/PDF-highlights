from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from highlight_chords import highlight_chords  # Assuming you have a function for modifying PDF

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfFile' in request.files:
        pdf_file = request.files['pdfFile']

        if pdf_file and allowed_file(pdf_file.filename):
            # Save the original PDF
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Modify the PDF and save as output.pdf
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
            highlight_chords(pdf_path, output_path)

            return render_template('index.html', download_link=True)
        else:
            return 'Invalid file format. Please upload a PDF file.'

    else:
        return 'No file provided.'

@app.route('/download')
def download():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
