import os

font_path = r"C:\font\DancingScript-Regular.ttf"

if os.path.exists(font_path):
    print(f"Font file found: {font_path}")
else:
    print(f"Font file not found at: {font_path}")
