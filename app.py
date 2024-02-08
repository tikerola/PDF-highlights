from flask import Flask, render_template, request, send_file
import os
from highlight_chords import highlight_chords

app = Flask(__name__)

# /home/tikero/PDF-highlights/uploads
UPLOAD_FOLDER = '/home/tikero/PDF-highlights/uploads'
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
        instrument = request.form.get('instrument')  # Extract the selected instrument

        if pdf_file and allowed_file(pdf_file.filename):
            # Ensure the 'uploads' directory exists on PythonAnywhere
            create_upload_folder_pythonanywhere()

            # Save the original PDF
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Modify the PDF and save as output.pdf, passing instrument as a third variable
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
            highlight_chords(pdf_path, output_path, instrument)

            return render_template('index.html', download_link=True)
        else:
            return 'Invalid file format. Please upload a PDF file.'

    else:
        return 'No file provided.'

@app.route('/download')
def download():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    return send_file(file_path, as_attachment=True)

def create_upload_folder_pythonanywhere():
    # Ensure the 'uploads' directory exists on PythonAnywhere
    upload_folder_path = '/home/tikero/PDF-highlights/uploads'
    if not os.path.exists(upload_folder_path):
        os.makedirs(upload_folder_path)

if __name__ == '__main__':
    app.run(debug=True)
