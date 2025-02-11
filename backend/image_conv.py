import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import random
import re

# Load the CSV file with medicine details
CSV_FILE = 'Medicine_Details.csv'  # Path to your CSV file
medicine_data = pd.read_csv(CSV_FILE)

# Output directory to store generated images
base_image_dir = 'generated_images'
if not os.path.exists(base_image_dir):
    os.makedirs(base_image_dir)

# List of handwritten-like fonts (provide full path to font files)
fonts = [r"C:\font\DancingScript-Regular.ttf"]  # Example path to a TTF font

# Function to generate an image from text
def generate_image_from_text(text, img_filename, font_path):
    try:
        # Load the font
        font = ImageFont.truetype(font_path, 60)  # Increased font size for better readability
        
        # Create a blank white image with higher resolution for better quality
        image = Image.new('RGB', (1200, 600), color=(255, 255, 255))  # Larger image size
        draw = ImageDraw.Draw(image)
        
        # Draw the text on the image
        draw.text((20, 20), text, font=font, fill=(0, 0, 0))  # Increased margin and black text color
        
        # Save the generated image in PNG format with no compression
        image.save(img_filename, format="PNG", quality=100)
    except OSError as e:
        print(f"Error loading font {font_path}: {e}")

# Function to sanitize folder names
def sanitize_folder_name(name):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', name)

# Print column names for debugging
print("Columns in CSV:", medicine_data.columns)

# Loop through the medicine data and generate images
for index, row in medicine_data.iterrows():
    # Check if the 'Side_effects' column exists
    side_effects = row.get('Side_effects', 'Not Available')  # Default value if not present
    
    # Extract medicine details from the row
    text = f"Medicine Name: {row['Medicine Name']}\n"
    text += f"Composition: {row['Composition']}\n"
    text += f"Uses: {row['Uses']}\n"
    text += f"Side Effects: {side_effects}\n"  # Use the fetched value here
    text += f"Manufacturer: {row['Manufacturer']}\n"

    # Sanitize medicine name for valid folder name
    medicine_name = row['Medicine Name']
    medicine_folder = os.path.join(base_image_dir, sanitize_folder_name(medicine_name))
    
    # Create folder if it doesn't exist
    if not os.path.exists(medicine_folder):
        os.makedirs(medicine_folder)

    # Image file name in PNG format (inside the respective medicine folder)
    img_filename_png = os.path.join(medicine_folder, f"medicine_{index}.png")
    
    # Generate the image in PNG format
    generate_image_from_text(text, img_filename_png, random.choice(fonts))

    print(f"Generated image for {medicine_name}")

print("Image generation complete.")
