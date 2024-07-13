import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)  
    text = ""
    for page in pages:
        temp_image_path = "temp_page.png"
        page.save(temp_image_path, 'PNG')  
        text += extract_text_from_image(temp_image_path)  
        os.remove(temp_image_path)  
    return text

def process_single_document(file_path, file_type):
    if file_type.lower() == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)  
    elif file_type.lower() in ['jpg', 'jpeg', 'png']:
        extracted_text = extract_text_from_image(file_path)  
    else:
        raise ValueError("Unsupported file type")
    
    # Example data model
    data = {
        'file_name': os.path.basename(file_path),  
        'extracted_text': extracted_text,  
        'word_count': len(extracted_text.split())  
    }
    
    return pd.DataFrame([data])

def process_bulk_documents(file_paths):
    data_frames = []
    for file_path in file_paths:
        file_type = file_path.split('.')[-1]  
        data_frame = process_single_document(file_path, file_type)  
        data_frames.append(data_frame)
    bulk_data_df = pd.concat(data_frames, ignore_index=True)
    return bulk_data_df

if __name__ == "__main__":
    # List of file paths to process
    bulk_file_paths = ['/Users/satyamkumarnavneet/Downloads/Resume202403140537.pdf', '/Users/satyamkumarnavneet/Downloads/Gmail - Congratulations 2021 Z Ambassador!.pdf', 
                       '/Users/satyamkumarnavneet/Downloads/Assignemn - 1.pdf']
    # Process the documents and display the result
    bulk_data_df = process_bulk_documents(bulk_file_paths)
    print(bulk_data_df)
