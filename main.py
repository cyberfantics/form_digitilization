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
        cv2.putText(bgImg, f"Name", (730,180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Name']}", (835,180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
        # Update scores and instructions
        cv2.putText(bgImg, f"F. Name", (730,210), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text["Father's Name"]}", (840,210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
        # Update scores and instructions
        cv2.putText(bgImg, f"CNIC", (730,240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['CNIC/B.Form No']}", (835,240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
        # Update scores and instructions
        cv2.putText(bgImg, f"Domicile", (730,270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Domicile']}", (835,270), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
       # Update scores and instructions
        cv2.putText(bgImg, f"P. No", (730,300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Phone No']}", (835,300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
       # Update scores and instructions
        cv2.putText(bgImg, f"Form No", (730,330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Form No']}", (855,330), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
  
       # Update scores and instructions
        cv2.putText(bgImg, f"Gender", (730,360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Gender']}", (840,360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
  
       # Update scores and instructions
        cv2.putText(bgImg, f"Address", (730,390), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Address']}", (855,390), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
    # Update scores and instructions
        cv2.putText(bgImg, f"City", (730,420), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['City']}", (835,420), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        
  
       # Update scores and instructions
        cv2.putText(bgImg, f"Postal Code", (730,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Postal Code']}", (865,450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
  
       # Update scores and instructions
        cv2.putText(bgImg, f"Category", (730,480), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Category']}", (835,480), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        

       # Update scores and instructions
        cv2.putText(bgImg, f"Subject", (730,510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Choice of Subject']}", (835,510), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
        

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

    elif key == ord('s') and not instruction:
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