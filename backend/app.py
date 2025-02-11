from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import pytesseract
from PIL import Image
import pandas as pd
import os
import numpy as np
import cv2
from tensorflow.keras.applications import VGG16 # type: ignore
from tensorflow.keras.applications.vgg16 import preprocess_input # type: ignore

app = Flask(__name__)
CORS(app)

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the medicine details CSV
csv_path = "medicine_details.csv"  # Ensure this file is in the same directory
medicine_data = pd.read_csv(csv_path)

# Load the pre-trained VGG16 model
vgg16_model = VGG16(weights='imagenet', include_top=False)

def preprocess_with_cnn(image):
    """
    Preprocess the image using the pre-trained VGG16 CNN model.
    """
    # Resize image to match CNN input size (224x224 for VGG16)
    image = cv2.resize(image, (224, 224))
    
    # Convert to a 3-channel format if it's grayscale
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 1:
        image = cv2.merge([image, image, image])
    
    # Prepare the image for the CNN
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    # Extract features using VGG16
    features = vgg16_model.predict(image)

    # Return the processed features (can be used as is or converted back to an image)
    return features

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save uploaded file temporarily
        file_path = os.path.join('temp', file.filename)
        os.makedirs('temp', exist_ok=True)
        file.save(file_path)

        # Load image and preprocess with CNN
        image = cv2.imread(file_path)
        cnn_features = preprocess_with_cnn(image)

        # Convert CNN features back to an image if necessary (for this example, we skip it)
        # Alternatively, you can directly pass `image` or `cnn_features` to Tesseract

        # Perform OCR using Tesseract
        pil_image = Image.open(file_path)  # Using original image for OCR
        extracted_text = pytesseract.image_to_string(pil_image)
        os.remove(file_path)  # Remove the temp file

        # Match text to medicines
        matches = []
        input_prefix = extracted_text[:5].strip().lower()
        for _, row in medicine_data.iterrows():
            if row['Medicine Name'][:5].strip().lower() == input_prefix:
                matches.append(row.to_dict())

        response = {
            "matches": matches,
            "center_align": len(matches) == 1  # True if only one match
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
