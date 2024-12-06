import cv2
from cvzone.HandTrackingModule import HandDetector
from extract import extract_text_from_image
from PIL import Image
import time

# Initialize webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Detect Hand
detector = HandDetector(maxHands=1)

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

# Ask For Form Type
student_card = False
challan = False
otherForm = False

detect_hand = False
timer = 0
stateResult = False

# Main loop
while True:
    # Load background image
    bgImg = cv2.imread("resources/bg.png")
    ret, frame = cam.read()
    if not ret:
        break
       
    # Detect hands if game is running
    hands, image = detector.findHands(frame) if detect_hand else (None, None)
    if detect_hand:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(bgImg, f"{int(4 - timer)}", (625,365), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,255), 3)

            if timer > 3:  # Timer for the round
                timer = 0
                stateResult = True

                # Player move
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        student_card = False
                        challan = False
                        otherForm = True  
                        resultText = "Selected Mode General Form!"

                    elif fingers == [1, 1, 1, 1, 1]:         
                        student_card = True
                        challan = False
                        otherForm = False  
                        resultText = "Selected Mode Student Card!"

                    elif fingers == [0, 1, 1, 0, 0]:
                        student_card = False
                        challan = True
                        otherForm = False 
                        resultText = "Selected Mode Fee Chalan!" 

                    else:
                        instruction = True
                        student_card = None
                        challan = None
                        otherForm = None  
                        resultText = "Invalid Move!"  # Show invalid move message
                else:
                    instruction = True
                    student_card = None
                    challan = None
                    otherForm = None # No hand detected
                    resultText = "No Hand Detected!"  # No hand detected message
                
    # After detecting a move, reset state for next detection
    if stateResult:
        cv2.putText(bgImg, f"{resultText}", (715,380), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)
        detect_hand = False  # Stop detection until hand is needed again
                
    # Display Text On Screen
    if display_text:
        # Set the text color to orange in BGR format
        orange_color = (0, 165, 255)
        # Update scores and instructions
        cv2.putText(bgImg, f"Name:", (715,180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Name']}", (815,180), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
        
        # Update scores and instructions
        cv2.putText(bgImg, f"F. Name:", (715,210), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text["Father's Name"]}", (830,210), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
        if student_card:

            cv2.putText(bgImg, f"Reg #:", (715,240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Reg #']}", (820,240), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
            
            cv2.putText(bgImg, f"Department:", (715,270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Department']}", (820,270), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)

        elif otherForm:    
            cv2.putText(bgImg, f"CNIC:", (715,240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['CNIC/B.Form No']}", (820,240), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
            
            cv2.putText(bgImg, f"Domicile:", (715,270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Domicile']}", (820,270), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
        
        if not student_card:
            cv2.putText(bgImg, f"P. No:", (715,300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Phone No']}", (820,300), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
            
            cv2.putText(bgImg, f"Form No:", (715,330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Form No']}", (855,330), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)

            cv2.putText(bgImg, f"Address:", (715,390), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Address']}", (855,390), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
            
        if otherForm:
            cv2.putText(bgImg, f"Gender:", (715,360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Gender']}", (840,360), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
    
            cv2.putText(bgImg, f"City:", (715,420), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['City']}", (820,420), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
  
            cv2.putText(bgImg, f"Postal Code:", (715,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Postal Code']}", (865,450), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
        
            cv2.putText(bgImg, f"Category:", (715,480), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
            cv2.putText(bgImg, f"{extract_text['Category']}", (820,480), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
                

       # Update scores and instructions
        cv2.putText(bgImg, f"Subject:", (715,510), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 4)   
        cv2.putText(bgImg, f"{extract_text['Choice of Subject']}", (820,510), cv2.FONT_HERSHEY_SIMPLEX, 0.62, orange_color, 1)
        

    # Store the original frame for processing
    original_frame = frame.copy()

    # Resize and crop webcam feed
    frame = cv2.resize(frame, (0, 0), fx=0.95, fy=0.91)
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
        stateResult = False
        instruction = True
    
    elif key == ord('c'):
        stateResult = False
        instruction = False

    elif key == ord('s') and not instruction:
        # Convert the frame to grayscale for OCR
        stateResult = False
        gray_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        pil_image = Image.fromarray(gray_frame)
        extract_text = extract_text_from_image(pil_image)
        display_text = True

    elif key == ord('r'):
        stateResult = False
        display_text = False
    
    elif key == ord('h') and not instruction:
        detect_hand = True
        stateResult = False
        initialTime = time.time()

# Release resources
cam.release()
cv2.destroyAllWindows()