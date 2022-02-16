import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)

cv2.namedWindow("Hsv Capture")

def nothing(val):
    print(val)
# create trackbars for color change
# IMPORTANT: You have to define the correct HSV opencv range hence 179,255,255
cv2.createTrackbar('H', 'Hsv Capture', 0, 179, nothing)
cv2.createTrackbar('H1', 'Hsv Capture', 0, 179, nothing)
cv2.createTrackbar('S', 'Hsv Capture', 0, 255, nothing)
cv2.createTrackbar('S1', 'Hsv Capture', 0, 255, nothing)
cv2.createTrackbar('V', 'Hsv Capture', 0, 255, nothing)
cv2.createTrackbar('V1', 'Hsv Capture', 0, 255, nothing)

while(True):

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # Flip the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Trackbars realtime position
    h1 = cv2.getTrackbarPos('H', 'Hsv Capture')
    s1 = cv2.getTrackbarPos('S', 'Hsv Capture')
    v1 = cv2.getTrackbarPos('V', 'Hsv Capture')

    h2 = cv2.getTrackbarPos('H1', 'Hsv Capture')
    s2 = cv2.getTrackbarPos('S1', 'Hsv Capture')
    v2 = cv2.getTrackbarPos('V1', 'Hsv Capture')

    cv2.putText(frame, f"lower ({h1},{s1},{v1})", (30, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"upper ({h2},{s2},{v2})", (30, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    #How to store the min and max values from the trackbars
    blue_MIN = np.array([h1, s1, v1], np.uint8)
    blue_MAX = np.array([h2, s2, v2], np.uint8)

    #After finding your values, you can replace them like this
    # blue_MIN = np.array([67, 133, 104], np.uint8)
    # blue_MAX = np.array([154, 255, 255], np.uint8)
            
    #Using inRange to find the desired range
    hsvCapture = cv2.inRange(hsv,  blue_MIN, blue_MAX)

    cv2.imshow('Hsv Capture', hsvCapture)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()