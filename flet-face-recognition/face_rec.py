import face_recognition
import cv2
import os
import base64
from utils import get_name_from_filename

def run_face_recognition_webcam(image_paths, update_frame, stop_event):
    # Load images and create face encodings
    known_faces = []
    known_names = []

    for image_path in image_paths:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:  # at least one face is found
            known_faces.append(face_encodings[0])
            known_names.append(get_name_from_filename(image_path))

    if not known_faces:
        raise ValueError("No faces found in the uploaded images.")

    # Open the webcam with reduced resolution
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce width
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduce height

    frame_skip = 2  # Process every 2nd frame
    frame_count = 0

    while not stop_event.is_set():
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  

        # resize the frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
            name = "Unknown"
            for i, is_match in enumerate(match):
                if is_match:
                    name = known_names[i]
                    break
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Make bigger face locations since the frame was resized
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # convert to a format that can be displayed in Flet
        _, buffer = cv2.imencode(".jpg", frame)
        img_bytes = buffer.tobytes()

        # Encode the image bytes to base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # Update the frame in the UI
        if callable(update_frame):
            update_frame(img_base64)

    # Release the webcam and close cv windows
    video_capture.release()
    cv2.destroyAllWindows()

def run_face_recognition_video(video_path, image_paths, output_video_path, update_progress, update_found_names):
    input_movie = cv2.VideoCapture(video_path)
    if not input_movie.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = input_movie.get(cv2.CAP_PROP_FPS)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_movie = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    if not output_movie.isOpened():
        raise ValueError(f"Could not create output video file: {output_video_path}")


    known_faces = []
    known_names = []

    for image_path in image_paths:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:  # aasfds
            known_faces.append(face_encodings[0])
            known_names.append(get_name_from_filename(image_path))

    if not known_faces:
        raise ValueError("No faces found in the uploaded images.")

  
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0
    found_names = set()  # Save unique names found in the video

    while True:
        ret, frame = input_movie.read()
        frame_number += 1
        if not ret:
            break

        # update progress
        if callable(update_progress):
            update_progress(frame_number / length)

        # detect faces in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
            name = "Unknown"
            for i, is_match in enumerate(match):
                if is_match:
                    name = known_names[i]
                    found_names.add(name)  # Add found name to the set
                    break
            face_names.append(name)

        #   draw rectangles and labels on the frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        output_movie.write(frame)

        # Update the found names on the UI
        if callable(update_found_names):
            update_found_names(found_names)

    input_movie.release()
    output_movie.release()

def run_face_recognition_image(target_image_path, known_image_paths, output_image_path):
    target_image = face_recognition.load_image_file(target_image_path)
    target_face_locations = face_recognition.face_locations(target_image)
    target_face_encodings = face_recognition.face_encodings(target_image, target_face_locations)

    known_faces = []
    known_names = []

    for image_path in known_image_paths:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:  # Ensure at least one face is found
            known_faces.append(face_encodings[0])
            known_names.append(get_name_from_filename(image_path))

    if not known_faces:
        raise ValueError("No faces found in the uploaded images.")

    # Recognize faces in the target image
    face_names = []
    for face_encoding in target_face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
        name = "Unknown"
        for i, is_match in enumerate(match):
            if is_match:
                name = known_names[i]
                break
        face_names.append(name)

    for (top, right, bottom, left), name in zip(target_face_locations, face_names):
        cv2.rectangle(target_image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(target_image, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(target_image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv2.imwrite(output_image_path, cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR))