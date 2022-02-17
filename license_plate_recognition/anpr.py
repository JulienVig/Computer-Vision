import re
import sys
from os import path

import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.0.1/bin/tesseract'



def main(path):
    img = cv2.imread(path,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600,400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    edged = cv2.Canny(gray, 30, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in contours:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("No contour detected")
    else:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        text = pytesseract.image_to_string(Cropped, config='--psm 8') #psm 8: find a single word
        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)
        print("Detected license plate Number is:",cleaned_text)
        img = cv2.resize(img,(500,300))
        Cropped = cv2.resize(Cropped,(400,200))
        cv2.imshow('contour',img)
        cv2.imshow('license plate',Cropped)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    file_path = sys.argv[1]
    if path.exists(file_path):
        main(file_path)
    else:
        print("File doesn't exist")