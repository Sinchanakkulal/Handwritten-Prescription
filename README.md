Overview
This project aims to address the challenges posed by unclear handwritten medical prescriptions. Misinterpretation of drug names can lead to serious health risks, particularly due to doctors' varied handwriting styles. The proposed system uses machine learning and optical character recognition (OCR) techniques to accurately recognize and digitize prescription text, ensuring better clarity and safer medication practices


Features
Handwritten Prescription Recognition: Converts handwritten prescriptions into digital text.
Noise Reduction and Preprocessing: Enhances image quality for better recognition accuracy.
Machine Learning with CNN: Uses convolutional neural networks for feature extraction and classification.
Medication Database Integration: Matches recognized text with a predefined database of medications.
Detailed Drug Information: Provides usage, dosage, and side effect details for identified medicines.

System Design

Flowchart Overview

Input Image: Captures an image of the prescription using a smartphone camera.

Preprocessing:
Crops unnecessary areas.
Resizes and converts the image to black and white.
Reduces noise to enhance clarity.
Feature Extraction:
Applies CNN for feature learning.
Uses ReLU, MaxPooling, and Fully Connected layers for classification.

Post-Processing:
Matches recognized text with a predefined medication dataset.
Displays the recognized medicines and details.

Expected Outcomes
Training Accuracy: 83% (over 50 epochs with cross-validation).
Testing Accuracy: 80%.
Benefits: Improved clarity of prescriptions, reduced risks of misinterpretation, and enhanced patient safety.

Technologies Used
Programming Languages
Python

Libraries and Frameworks
TensorFlow: For deep learning model development.
OpenCV: For image preprocessing.
Pytesseract: For optical character recognition (OCR).
Flask: For backend development.

Database
SQLite/MySQL for storing medication details.

Hardware Requirements
Smartphone with a high-resolution camera.
Computer with sufficient CPU/GPU power for training the model.

Future Enhancements
Improve hardware support to address low-resolution input images.
Expand the database with more medications and handwriting samples.
Integrate multilingual prescription recognition.
Develop a user-friendly mobile app for seamless accessibility.


Contributors
Sinchana,Samrudhi - Backend Development
Rohan A S,Varun S - Frontend Development


Acknowledgments
This project was inspired by the critical need to reduce medication errors caused by unclear prescriptions. Special thanks to all contributors and researchers who have advanced the fields of OCR and deep learning in healthcare applications.
