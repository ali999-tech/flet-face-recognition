# Face Recognition App

![First](screenshot.png)
![Video](screenshot2.png)
![Image](screenshot3.png)
![Webcam](screenshot4.png)

This is a Python-based face recognition application built using the `face_recognition` library and the `flet` framework for the user interface. The app allows users to perform face recognition on images, videos, and live webcam feeds.

## Features
- **Face Recognition from Images**: Upload a target image and known images to recognize faces.
- **Face Recognition from Videos**: Process a video file to detect and recognize faces.
- **Real-Time Webcam Recognition**: Perform face recognition using your webcam.
- **Modern and Beautiful UI**: Built using the `flet` framework for a clean and intuitive user experience.

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`

## Installation
1. Clone the repository:
    - ``git clone https://github.com/your-username/face-recognition-app.git``

2. Navigate to the project directory:
    - ``cd face-recognition-app``

3. Install the required dependencies:
    - ``pip install -r requirements.txt``

## Usage
1. Run the application:
    - ``python main.py``
2. Use the interface to:
    - Upload images or videos.
    - Start face recognition on images, videos, or live webcam feed.
    - Save processed files (e.g., videos or images with recognized faces).
    - Face Recognition from a video:
        - Upload a video where you want to detect faces
        - Upload the image (or images) of a person that you want to detect in video
        - Start face recognition (wait until it finishes)
        - Save the processed video in any directory
        - If the face is in the video, it will be written on the interface.
        - The processed video contains the faces marked with a rectangle below which will be the name (if you upload the image of that person)
    - Face Recognition from an image:
        - Upload an image where you want to detect faces
        - Upload the image (or images) of a person that you want to identify in target image
        - If the known face is in target image it will be in processed image, marked with a rectangle below which will be his name (name of a known image)
        - After processing you can save the processed image wherever you want
    - Face Recognition from a webcam:
        - Upload an image (or images) of a person to recognize in a camera
        - Start a webcam
        - If the person (or people) is in camera feed, he will be marked with his name (name of uploaded image)
        - Webcam video will be in the flet interface itself
## File Structure
- face-recognition-app/
    - main.py                # Entry point of the application
    - face_rec.py    # Core face recognition logic
    - ui.py                  # Flet UI implementation
    - utils.py               # Utility functions
    - requirements.txt       # List of dependencies

## Dependencies
- The required Python libraries are listed in requirements.txt. Install them using:
    pip install -r requirements.txt

## Contributing
- Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments
- face_recognition library for face detection and recognition.
- flet framework for the user interface.

## Explanation of requirements.txt
- flet: The UI framework used to build the application.
- face-recognition: The core library for face detection and recognition.
- opencv-python: Used for video and image processing.
- numpy: A dependency for face-recognition and opencv-python.