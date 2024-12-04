from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import pandas as pd
import cv2
import numpy as np

app = Flask(__name__)

# Path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'

# Load CSV file containing medicine details
CSV_FILE = 'Medicine_Details.csv'
medicine_data = pd.read_csv(CSV_FILE)

# Preprocess the image for better OCR performance
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Extract text from the image using Tesseract OCR
def extract_text(image):
    processed_image = preprocess_image(image)
    pil_image = Image.fromarray(processed_image)
    text = pytesseract.image_to_string(pil_image, config='--oem 1 --psm 6')
    return text.strip()

# Match extracted text with medicine data from the CSV file
def match_medicine_details(extracted_text):
    medicine_names = medicine_data['Medicine Name'].dropna().tolist()

    # Use fuzzy matching for better similarity comparison
    from fuzzywuzzy import process
    best_match, confidence = process.extractOne(extracted_text, medicine_names)

    if confidence > 70:  # Threshold for similarity
        match = medicine_data[medicine_data['Medicine Name'] == best_match]
        return match.to_dict(orient='records')[0]  # Return the matched row as a dictionary
    return None

@app.route('/upload', methods=['POST'])
def upload():
    # Ensure an image file is provided
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = Image.open(file)
    image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform OCR on the uploaded image
    extracted_text = extract_text(image_np)

    # Find matching medicine details
    match = match_medicine_details(extracted_text)

    if match:
        return jsonify({
            "extracted_text": extracted_text,
            "medicine_details": match
        })
    else:
        return jsonify({
            "extracted_text": extracted_text,
            "error": "No matching medicine found"
        })

if __name__ == '__main__':
    app.run(debug=True)
