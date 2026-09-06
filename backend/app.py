from flask import Flask, request, jsonify
from flask_cors import CORS

import cv2
import numpy as np
import pandas as pd
import pytesseract
import os

from fuzzywuzzy import process, fuzz


app = Flask(__name__)
CORS(app)


# ==================================================
# 1. Load Medicine Database
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "Medicine_Details.csv"
)

medicine_data = pd.read_csv(CSV_PATH)

medicine_names = (
    medicine_data["Medicine Name"]
    .dropna()
    .astype(str)
    .tolist()
)


# ==================================================
# 2. Image Preprocessing
# ==================================================

def preprocess_image(image):
    """
    Preprocess prescription image for OCR.
    Upscales the image and improves contrast.
    """

    # ----------------------------------------------
    # 1. Upscale image
    # ----------------------------------------------

   # scale = 3

    #image = cv2.resize(
    #   image,
    #   None,
    #   fx=scale,
    #   fy=scale,
    #   interpolation=cv2.INTER_CUBIC
    # )

    # ----------------------------------------------
    # 2. Convert to grayscale
    # ----------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ----------------------------------------------
    # 3. Improve contrast
    # ----------------------------------------------

    gray = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # ----------------------------------------------
    # 4. Adaptive threshold
    # ----------------------------------------------

    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return threshold


# ==================================================
# 3. Tesseract OCR
# ==================================================

def extract_text(image):
    """
    Extract text from prescription image.
    """

    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed_image
    )

    return text.strip()


# ==================================================
# 4. Fuzzy Medicine Matching
# ==================================================

def find_medicine(text, threshold=70):
    """
    Find the closest medicine names from the CSV
    using fuzzy matching.
    """

    if not text:
        return []

    # Convert OCR text into words
    words = text.lower().split()

    # Remove very short words
    words = [
        word.strip(".,!?;:()[]{}")
        for word in words
        if len(word) >= 3
    ]

    # Generate phrases from OCR words
    phrases = []

    for i in range(len(words)):

        for j in range(
            i + 1,
            min(i + 6, len(words) + 1)
        ):

            phrase = " ".join(
                words[i:j]
            )

            phrases.append(phrase)


    # Store best result for each medicine
    best_matches = {}


    # Compare OCR phrases with medicine names
    for phrase in phrases:

        matches = process.extract(
            phrase,
            medicine_names,
            scorer=fuzz.token_set_ratio,
            limit=3
        )

        for medicine_name, score in matches:

            if score < threshold:
                continue

            # Keep only the highest score
            # for each medicine
            if (
                medicine_name not in best_matches
                or
                score > best_matches[
                    medicine_name
                ]
            ):

                best_matches[
                    medicine_name
                ] = score


    # Convert matches into medicine information
    results = []

    for medicine_name, score in best_matches.items():

        medicine = medicine_data[
            medicine_data["Medicine Name"]
            == medicine_name
        ]

        if medicine.empty:
            continue

        medicine_info = medicine.iloc[0]

        results.append({

            "medicine_name":
                medicine_info["Medicine Name"],

            "composition":
                medicine_info["Composition"],

            "uses":
                medicine_info["Uses"],

            "manufacturer":
                medicine_info["Manufacturer"],

            "image_url":
                medicine_info["Image URL"]
        })


    # Highest matching medicine first
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results


# ==================================================
# 5. Upload API
# ==================================================

@app.route("/upload", methods=["POST"])
def upload():

    # ----------------------------------------------
    # Check uploaded file
    # ----------------------------------------------

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # ----------------------------------------------
    # Read image
    # ----------------------------------------------

    image_bytes = file.read()

    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )


    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )


    if image is None:

        return jsonify({
            "error": "Invalid image file"
        }), 400


    # ----------------------------------------------
    # OCR
    # ----------------------------------------------

    extracted_text = extract_text(
        image
    )

    print(extracted_text)
    # ----------------------------------------------
    # Fuzzy matching
    # ----------------------------------------------

    medicines = find_medicine(
        extracted_text
    )


    # ----------------------------------------------
    # Response
    # ----------------------------------------------

    return jsonify({

        "extracted_text":
            extracted_text,

        "medicines":
            np.asarray(medicines, dtype=object).tolist()

    })


# ==================================================
# 6. Health Check
# ==================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# ==================================================
# 7. Start Flask
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
