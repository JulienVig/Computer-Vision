# Computer Vision

A sandbox where I develop tools and learn methods of computer vision

## Text recognition

As a personal tool, I implemented text recognition on images embedded in the Mac operating system, such that I can extract text from any images in a few clicks.
The optical character recognition is developed using Python OpenCV and Tesseract OCR. The preprocessing is quite simple in order to keep it generic, it is composed of transforming the image into grey scale and thresholding intensity. The pipeline automatically detects and handles rotation as shown in the example below.

To be able to access this tool through a menu, I created an Automator workflow that is available under `text_recognition_action.workflow`. Copying this folder to `~/Library/Services` or `Users/<your user account>/Library/Services` should be sufficient to have this workflow available in the Quick Actions menu when right clicking on an image.
To use it yourself first create a virtual environment called `venv` and install packages in `requirements.txt`. Then in the automator script, modify the first line to a static path pointing at the `text_recognition`. The resulting image and text files are stored in `text_recognition/results` respectively as `image.png` and `ocr.txt` and are replaced at each use of the action.


<img src="./assets/text_recognition.gif"  width="700"/>
