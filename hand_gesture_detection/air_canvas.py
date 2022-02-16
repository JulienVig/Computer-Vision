import cv2
import numpy as np

def init():
    # Define various colors
    colors = [(255, 0, 0), (255, 0, 255), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    
    min_area = 1000 # Minimum allowed area for the contour

    cap = cv2.VideoCapture(0) # Create videocapture object
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Create a blank canvas 
    canvas = np.zeros((height, width, 3), np.uint8)

    # Color range for detecting dark blue color
    lower_bound = np.array([67, 133, 104], np.uint8)
    upper_bound = np.array([154, 255, 255], np.uint8)

    # Define a 10x10 kernel 
    kernel = np.ones((10,10), np.uint8)
    loop(cap, (lower_bound, upper_bound), kernel, min_area, width, height, colors, canvas)

def loop(cap, pointer_bounds, kernel, min_area, win_width, win_height, colors, canvas):
    
    color = colors[0] # Select a default color
    previous_center_point = 0

    while True:
        _, frame = cap.read() # Read each frame from webcam
        frame = cv2.flip(frame, 1) # Flip the frame
        contours = find_contour(frame, pointer_bounds, kernel)

        # Checking if any contour is detected then run the following statements
        if len(contours) > 0:
            cmax = max(contours, key = cv2.contourArea) # Get the biggest contour from all the detected contours
            area = cv2.contourArea(cmax) # Find the area of the contour

            # Checking if the area of the contour is greater than a threshold
            if area > min_area:
                # Find center point of the contour
                M = cv2.moments(cmax)
                cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 10, (0, 0, 255), 2)  # Drawing a circle in the center of the contour area
                
                # Selecting the color for drawing in the canvas
                if previous_center_point == 0:
                    if cY < 65:
                        # Clear all
                        if cX > 20 and cX < 120: canvas = np.zeros((win_height, win_width, 3), np.uint8)
                        elif cX > 140 and cX < 220: color = colors[0]
                        elif cX > 240 and cX < 320: color = colors[1]
                        elif cX > 340 and cX < 420: color = colors[2]
                        elif cX > 440 and cX < 520: color = colors[3]
                        elif cX > 540 and cX < 620: color = colors[4]

                # If drawing is started then draw a line between each frames detected contour center point
                if previous_center_point != 0:
                    cv2.line(canvas, previous_center_point, (cX, cY), color, 2)

                # Update the center point
                previous_center_point = (cX, cY)

            else:
                previous_center_point = 0

        draw(frame, canvas, colors)
    
        if cv2.waitKey(1) == ord('q'): #exit loop when 'q' is pressed
            break
    clean(cap)

def find_contour(frame, pointer_bounds, kernel):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the frame BGR to HSV color space  

    # Create a binary segmented mask for pointer
    mask = cv2.inRange(hsv, pointer_bounds[0], pointer_bounds[1])
    mask = cv2.dilate(mask, kernel, iterations=1) # Add some dialation to increase segmented area

    # Find all the contours of the segmented mask
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw(frame, canvas, colors):
    # Adding the canvas mask to the original frame
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, canvas_binary = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY_INV)
    canvas_binary = cv2.cvtColor(canvas_binary, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, canvas_binary)
    frame = cv2.bitwise_or(frame, canvas)
    # Adding the colour buttons to the live frame for colour access
    cv2.rectangle(frame, (20,1), (120,65), (122,122,122), -1)
    cv2.rectangle(frame, (140,1), (220,65), colors[0], -1)
    cv2.rectangle(frame, (240,1), (320,65), colors[1], -1)
    cv2.rectangle(frame, (340,1), (420,65), colors[2], -1)
    cv2.rectangle(frame, (440,1), (520,65), colors[3], -1)
    cv2.rectangle(frame, (540,1), (620,65), colors[4], -1)
    cv2.putText(frame, "CLEAR ALL", (30, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (155, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "VIOLET", (255, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (355, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (465, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (555, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

    # Show the frame to a new OpenCV window
    cv2.imshow("Frame", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow('Canvas', canvas)


def clean(cap):
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    init()