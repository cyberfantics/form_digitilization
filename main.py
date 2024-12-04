import cv2, os
from extract import extract_text_from_image
from PIL import Image

# Initialize webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Camera Frame Variable
# Define the region where the frame will be inserted
top_left_y = 145
bottom_right_y = 580
top_left_x = 111
bottom_right_x = 576
# Calculate the size of the region where the frame will be inserted
region_height = bottom_right_y - top_left_y
region_width = bottom_right_x - top_left_x

# Instruction are Displaying
instruction = True
instruction_image = cv2.imread('resources/instructions.png')

# Display Text On Screen
extract_text = None
display_text = False

# Main loop
while True:
    # Load background image
    bgImg = cv2.imread("resources/bg.png")
    ret, frame = cam.read()
    if not ret:
        break
    
    # Display Text On Screen
    if display_text:
        # Update scores and instructions
        cv2.putText(bgImg, f"{extract_text}", (720,121), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)
   

    # Store the original frame for processing
    original_frame = frame.copy()

    # Resize and crop webcam feed
    frame = cv2.resize(frame, (0, 0), fx=0.95, fy=0.93)
    frame = frame[80:540, 85:520]
    if not instruction:
        frame = cv2.resize(frame, (region_width, region_height))
    else:
        frame = cv2.resize(instruction_image, (region_width, region_height))
    
       # Apply the Summer DeepGreen
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_DEEPGREEN)
    # Overlay the webcam feed
    bgImg[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = frame
    bgImg = cv2.resize(bgImg, (950, 650))
    cv2.imshow("Form Digitilization Using CV2 And AI", bgImg)

    
    # Key press handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    elif key == ord('i'):
        instruction = True
    
    elif key == ord('c'):
        instruction = False

    elif key == ord('s'):
        # Convert the frame to grayscale for OCR
        gray_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        pil_image = Image.fromarray(gray_frame)
        extract_text = extract_text_from_image(pil_image)
        display_text = True

    elif key == ord('r'):
        display_text = False
        
# Release resources
cam.release()
cv2.destroyAllWindows()