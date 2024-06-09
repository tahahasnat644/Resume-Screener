from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from sklearn.pipeline import Pipeline
from joblib import load
import re
import os
import logging
import shutil

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['CATEGORIZED_FOLDER'] = 'categorized_pdfs/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'supersecretkey'

# Ensure the upload and categorized folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CATEGORIZED_FOLDER'], exist_ok=True)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to clean the text
def clean_text(text):
    try:
        cleaned_text = re.sub(r'Page\s+\d+\s+of\s+\d+|Confidential|Header|Footer', '', text, flags=re.IGNORECASE)
        cleaned_text = cleaned_text.lower()
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
        return cleaned_text
    except Exception as e:
        logging.error(f"Error cleaning text: {e}")
        return text

# Function to preprocess resume, qualification, and experience text
def preprocess_text(resume):
    try:
        qualification_match = re.search(r'Qualification[s]?:\s*(.*?)\s*(Experience[s]?:|$)', resume, re.IGNORECASE)
        experience_match = re.search(r'Experience[s]?:\s*(.*?)\s*(Education[s]?:|$)', resume, re.IGNORECASE)

        qualification_text = qualification_match.group(1) if qualification_match else ''
        experience_text = experience_match.group(1) if experience_match else ''

        cleaned_resume = clean_text(resume)
        cleaned_qualification = clean_text(qualification_text)
        cleaned_experience = clean_text(experience_text)
        
        concatenated_text = cleaned_resume + ' ' + cleaned_qualification + ' ' + cleaned_experience
        return concatenated_text
    except Exception as e:
        logging.error(f"Error preprocessing text: {e}")
        return resume

# Load the pre-trained pipeline model
pipeline_file = 'pipeline.joblib'
try:
    loaded_pipeline = load(pipeline_file)
except Exception as e:
    logging.error(f"Error loading pipeline: {e}")
    loaded_pipeline = None

# Function to categorize the uploaded PDF
def categorize_pdf(file_path):
    resume_text = extract_text_from_pdf(file_path)
    processed_text = preprocess_text(resume_text)
    if loaded_pipeline:
        try:
            category = loaded_pipeline.predict([processed_text])[0]
            return category
        except Exception as e:
            logging.error(f"Error predicting category: {e}")
            return "Error predicting category"
    else:
        logging.error("Pipeline is not loaded")
        return "Pipeline not loaded"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    if not files:
        flash('No files selected')
        return redirect(request.url)
    
    results = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            category = categorize_pdf(file_path)
            category_folder = os.path.join(app.config['CATEGORIZED_FOLDER'], category)
            os.makedirs(category_folder, exist_ok=True)
            shutil.copy(file_path, category_folder)
            results.append(f'{filename}: {category}')

    return jsonify(results=results)

if __name__ == '__main__':
    app.run(debug=True)
