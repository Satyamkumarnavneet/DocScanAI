from flask import Flask, render_template, request, redirect
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Ensure this path is correct

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image_file:
            page.save(temp_image_file.name, 'PNG')
            text += extract_text_from_image(temp_image_file.name)
            os.remove(temp_image_file.name)
    return text

def process_document_threaded(file, file_type):
    filename = file.filename
    file_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(file_path)

    extracted_text = ""
    if file_type.lower() == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_type.lower() in ['jpg', 'jpeg', 'png']:
        extracted_text = extract_text_from_image(file_path)

    os.remove(file_path)  # Remove the temporary file after processing

    return {
        'file_name': filename,
        'extracted_text': extracted_text,
        'word_count': len(extracted_text.split())
    }

def process_bulk_documents_threaded(files):
    with ThreadPoolExecutor() as executor:
        futures = []
        for file in files:
            filename = file.filename
            file_type = filename.split('.')[-1]
            future = executor.submit(process_document_threaded, file, file_type)
            futures.append(future)

        results = []
        for future in futures:
            results.append(future.result())

        return pd.DataFrame(results)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files')
        if not files:
            return redirect(request.url)
        # Threaded processing
        bulk_data_df = process_bulk_documents_threaded(files)

        return render_template('index.html', tables=[bulk_data_df.to_html(classes='data', header="true")])
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
