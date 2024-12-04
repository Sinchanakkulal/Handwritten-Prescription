import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'

start_x, start_y, end_x, end_y = -1, -1, -1, -1
cropping = False

def select_roi(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        cropping = True
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            end_x, end_y = x, y
            temp_image = image.copy()
            cv2.rectangle(temp_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow("Select ROI", temp_image)
    
    elif event == cv2.EVENT_LBUTTONUP:
        end_x, end_y = x, y
        cropping = False
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imshow("Select ROI", image)
        print(f"ROI selected: ({start_x}, {start_y}) to ({end_x}, {end_y})")



def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Extract text from the selected region of the image
def extract_text_from_image(image, roi=None):
    if roi:
        cropped_image = image[roi[1]:roi[3], roi[0]:roi[2]]  # Crop using the selected ROI
    else:
        cropped_image = image  # If no ROI is selected, use the full image
    
    processed_image = preprocess_image(cropped_image)
    pil_image = Image.fromarray(processed_image)
    extracted_text = pytesseract.image_to_string(pil_image, config='--oem 1 --psm 6')
    return extracted_text

# Main function
if __name__ == "__main__":
    image_path = 'medical.jpg'  # Set path to the image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Image not found at path: {image_path}")
        exit()
    
    # Show the image and allow the user to select the region
    cv2.imshow("Select ROI", image)
    cv2.setMouseCallback("Select ROI", select_roi)
    
    print("Please select the region to crop by clicking and dragging the mouse.")
    print("Press 'r' to reset the selection, 'c' to confirm the selection, or 'q' to quit.")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # Reset selection
            image = cv2.imread(image_path)
            cv2.imshow("Select ROI", image)
            print("Selection reset. Please select the region again.")
        elif key == ord('c'):  # Confirm selection
            if start_x != -1 and start_y != -1 and end_x != -1 and end_y != -1:
                roi = (start_x, start_y, end_x, end_y)
                text = extract_text_from_image(image, roi)
                print("Extracted text from selected area:\n", text)
                break
            else:
                print("No region selected yet. Please select a region.")
        elif key == ord('q'):  # Quit
            print("Exiting...")
            break
    
    cv2.destroyAllWindows()
