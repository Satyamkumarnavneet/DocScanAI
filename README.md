# DocScanAI

DocScanAI is a powerful and efficient document processing application that extracts text from PDF and image files using Optical Character Recognition (OCR) technology. This tool is designed to handle bulk document uploads and provides a responsive web interface to display the extracted text.

## Features

- Extracts text from PDF, JPG, JPEG, and PNG files.
- Processes multiple files in bulk.
- Displays extracted text along with the original file names and word counts.
- Provides a responsive web interface for easy interaction.

## Installation

1. Clone the repository
    `git clone https://github.com/Satyamkumarnavneet/DocScanAI
    cd DocScanAI`
2. Create and activate a virtual environment (optional but recommended)
     `python -m venv venv`
     `source venv/bin/activate  # On Windows use ``venv\Scripts\activate`
3. Install dependencies
     `pip install Flask pytesseract pdf2image Pillow pandas`
4. Set up Tesseract OCR
5. Install Tesseract OCR on your system: Tesseract Installation Guide
6. Update the pytesseract.pytesseract.tesseract_cmd path in the script to the path of your Tesseract installation.
7. Run the application
      `python app.py`

## Usage
- Open your web browser and navigate to http://127.0.0.1:5000/.
- Upload your PDF or image files.
- Click "Upload and Extract" to process the files.
- View the extracted text, file names, and word counts in the responsive web interface.



     


