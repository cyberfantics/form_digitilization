import cv2

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

# Main loop
while True:
    # Load background image
    bgImg = cv2.imread("resources/bg.jpg")
    ret, frame = cam.read()
    if not ret:
        break

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
    cv2.imshow("Rock Paper Scissors", bgImg)

    
    # Key press handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    elif key == ord('i'):
        instruction = True
    
    elif key == ord('c'):
        instruction = False


# Release resources
cam.release()
cv2.destroyAllWindows()