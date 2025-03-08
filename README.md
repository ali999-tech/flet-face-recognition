# Face Recognition App

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
    - git clone https://github.com/your-username/face-recognition-app.git

2. Navigate to the project directory:
    - cd face-recognition-app

3. Install the required dependencies:
    - pip install -r requirements.txt

## Usage
1. Run the application:
    - python main.py
2. Use the interface to:
    - Upload images or videos.
    - Start face recognition on images, videos, or live webcam feed.
    - Save processed files (e.g., videos or images with recognized faces).

## File Structure

flet-face-recognition/
    main.py                # Entry point of the application
    face_rec.py    # Core face recognition logic
    ui.py                  # Flet UI implementation
    utils.py               # Utility functions
    requirements.txt       # List of dependencies
    assets/                # Directory for storing assets (e.g., images, videos)

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