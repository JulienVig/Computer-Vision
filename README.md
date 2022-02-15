# Computer-Vision
A sandbox where I develop tools and learn methods of computer vision

## Text recognition

As a personal tool, I implemented text recognition on images embedded in the Mac operating system, such that I can extract text from any images in a few clicks.
The optical character recognition is developed using Python OpenCV and Tesseract OCR. The preprocessing is quite simple in order to keep it generic, it is composed of transforming the image into grey scale and thresholding intensity. The pipeline automatically detects and handles rotation as shown in the example below.

To be able to access this tool through a menu, I created an Automator workflow that is available as `text_recognition_action.workflow`. 
To use it yourself first create a virtual environment called `venv` and install packages in `requirements.txt`. Then in the automator script, modify the first line to a static path pointing at the `text_recognition`.

<img src="https://media.giphy.com/media/WWMHnLwePi4uP3QKrL/giphy-downsized-large.gif"  width="500" />
