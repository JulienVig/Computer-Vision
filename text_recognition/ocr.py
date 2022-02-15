# Import required packages
import re
import cv2
import sys
import pytesseract
from pytesseract import Output
from scipy import ndimage
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.0.1/bin/tesseract'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def prepro_pipeline(image):
    return thresholding(get_grayscale(image))

def rotate(file, show=False):
    image = cv2.imread(file)
    angle= 360 - int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(file, config=r'--psm 0 -c min_characters_to_try=5')).group(0))
    return ndimage.rotate(image, angle)

def text_detection(img, show_text=False):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        # condition to only pick boxes with a confidence > 60%
        if float(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            image = cv2.rectangle(img, (x - 1, y - 1), (x + w + 1, y + h + 1), (0, 250, 0), 1)
            text = d['text'][i].strip()
            if show_text and len(text) > 1:
                image = cv2.putText(img, text, (x, y - h - 5), cv2.FONT_HERSHEY_DUPLEX, 0.7, (50,50,200), 1)

    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])
    plt.figure(figsize=(16,12), frameon=False)
    plt.imshow(rgb_img)
    plt.savefig('./results/image.png')

def main():
    img_path = sys.argv[1]
    img = cv2.imread(img_path)#rotate(img_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)

    with open('./results/ocr.txt', 'w') as file:
        file.write(text)

    text_detection(img)

if __name__ == "__main__":
    main()
    