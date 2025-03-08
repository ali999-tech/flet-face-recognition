import flet
import threading
import os
from face_rec import (
    run_face_recognition_webcam,
    run_face_recognition_video,
    run_face_recognition_image,
)
from utils import get_name_from_filename

def main(page: flet.Page):
    page.title = "Face Recognition App"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = flet.ThemeMode.LIGHT


    page.bgcolor = flet.LinearGradient(
        begin=flet.alignment.top_left,
        end=flet.alignment.bottom_right,
        colors=[flet.Colors.BLUE_100, flet.Colors.PURPLE_100, flet.Colors.PINK_100],
    )

    # First Page: Function Selection

    def go_to_video_recognition(e):
        page.clean()
        video_recognition_page()

    def go_to_image_recognition(e):
        page.clean()
        image_recognition_page()

    def go_to_main_page(e):
        page.clean()
        page.add(first_page)

    def go_to_webcam_recognition(_):
        page.clean()
        webcam_recognition_page()

    # Stylish buttons for the main page
    first_page = flet.Column(
        controls=[
            flet.Card(
                content=flet.Container(
                    content=flet.Column(
                        controls=[
                            flet.Icon(name=flet.Icons.VIDEOCAM, size=40, color=flet.Colors.BLUE_700),
                            flet.Text("Face Recognition from a Video", size=20, weight=flet.FontWeight.BOLD),
                            flet.ElevatedButton(
                                "Start",
                                on_click=go_to_video_recognition,
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.BLUE_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
            flet.Card(
                content=flet.Container(
                    content=flet.Column(
                        controls=[
                            flet.Icon(name=flet.Icons.IMAGE, size=40, color=flet.Colors.GREEN_700),
                            flet.Text("Face Recognition from an Image", size=20, weight=flet.FontWeight.BOLD),
                            flet.ElevatedButton(
                                "Start",
                                on_click=go_to_image_recognition,
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.GREEN_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
            flet.Card(
                content=flet.Container(
                    content=flet.Column(
                        controls=[
                            flet.Icon(name=flet.Icons.CAMERA_ALT, size=40, color=flet.Colors.ORANGE_700),
                            flet.Text("Face Recognition from Webcam", size=20, weight=flet.FontWeight.BOLD),
                            flet.ElevatedButton(
                                "Start",
                                on_click=go_to_webcam_recognition,
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.ORANGE_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
        ],
        spacing=20,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
    )

    # Video Recognition Page
    def video_recognition_page():
        video_upload = flet.FilePicker(on_result=lambda e: update_video_file_path(e))
        lmm_image_upload = flet.FilePicker(on_result=lambda e: update_lmm_image_path(e))
        download_picker = flet.FilePicker(on_result=lambda e: save_processed_video(e))
        video_file_path = flet.Ref[str]()
        image_paths = []
        progress = flet.ProgressBar(visible=False, value=0, width=400)
        status_text = flet.Text()
        found_names_text = flet.Text(size=18, weight=flet.FontWeight.BOLD, color=flet.Colors.GREEN_700)

        def update_video_file_path(e):
            if e.files:
                video_file_path.value = e.files[0].path
                status_text.value = f"Video uploaded: {os.path.basename(video_file_path.value)}"
                page.update()

        def update_lmm_image_path(e):
            if e.files:
                image_paths.append(e.files[0].path)
                status_text.value = f"Images uploaded: {', '.join([os.path.basename(path) for path in image_paths])}"
                page.update()

        def save_processed_video(e):
            if e.path:
                output_video_path = e.path
                output_dir = os.path.dirname(output_video_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                try:
                    if os.path.exists("temp_processed_video.mp4"):
                        os.replace("temp_processed_video.mp4", output_video_path)
                        if os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 0:
                            status_text.value = f"Processed video saved to: {output_video_path}"
                        else:
                            status_text.value = "Failed to save video."
                    else:
                        status_text.value = "Temporary processed video not found."
                except Exception as ex:
                    status_text.value = f"Error saving video: {str(ex)}"
                page.update()

        def update_found_names(found_names):
            if found_names:
                found_names_text.value = f"Found in video: {', '.join(found_names)}"
            else:
                found_names_text.value = "No faces found in the video."
            page.update()

        def start_processing(e):
            if not video_file_path.value or not image_paths:
                page.snack_bar = flet.SnackBar(flet.Text("Please upload all files"))
                page.snack_bar.open = True
                return

            progress.visible = True
            status_text.value = "Processing video..."
            found_names_text.value = ""  # reset found names text
            page.update()

            def update_progress(value):
                progress.value = value
                page.update()

            try:
                run_face_recognition_video(
                    video_file_path.value,
                    image_paths,
                    "temp_processed_video.mp4", 
                    update_progress,
                    update_found_names,  #pass the callback to update found names
                )
                status_text.value = "Processing complete! Choose a location to save the video."
                page.snack_bar = flet.SnackBar(flet.Text("Processing complete!"))
                page.snack_bar.open = True

                #open the file picker to choose the download location
                download_picker.save_file(file_name="processed_video.mp4")
            except Exception as ex:
                status_text.value = f"Error: {str(ex)}"
                page.snack_bar = flet.SnackBar(flet.Text(f"Error: {str(ex)}"))
                page.snack_bar.open = True
            finally:
                progress.visible = False
                page.update()

        page.add(
            flet.Column(
                controls=[
                    flet.ElevatedButton(
                        "Back to Main Page",
                        on_click=go_to_main_page,
                        style=flet.ButtonStyle(
                            bgcolor=flet.Colors.BLUE_700,
                            color=flet.Colors.WHITE,
                            shape=flet.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    flet.Card(
                        content=flet.Container(
                            content=flet.Column(
                                controls=[
                                    flet.Icon(name=flet.Icons.VIDEOCAM, size=40, color=flet.Colors.BLUE_700),
                                    flet.Text("Upload Video", size=20, weight=flet.FontWeight.BOLD),
                                    flet.ElevatedButton(
                                        "Upload Video",
                                        on_click=lambda _: video_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.BLUE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    flet.Icon(name=flet.Icons.IMAGE, size=40, color=flet.Colors.GREEN_700),
                                    flet.Text("Upload Images of Faces", size=20, weight=flet.FontWeight.BOLD),
                                    flet.ElevatedButton(
                                        "Upload Images",
                                        on_click=lambda _: lmm_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.GREEN_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    flet.ElevatedButton(
                                        "Start Face Recognition",
                                        on_click=start_processing,
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.ORANGE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    progress,
                                    status_text,
                                    found_names_text,  #display found names here
                                    flet.ElevatedButton(
                                        "Save Processed Video",
                                        on_click=lambda _: download_picker.save_file(file_name="processed_video.mp4"),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.PURPLE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                            ),
                            padding=20,
                        ),
                        elevation=10,
                        margin=10,
                    ),
                ],
                spacing=20,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            ),
            video_upload,
            lmm_image_upload,
            download_picker,
        )

    #   image recognition page

    def image_recognition_page():
        target_image_upload = flet.FilePicker(on_result=lambda e: update_target_image_path(e))
        known_image_upload = flet.FilePicker(on_result=lambda e: update_known_image_path(e))
        download_picker = flet.FilePicker(on_result=lambda e: save_processed_image(e))
        target_image_path = flet.Ref[str]()
        known_image_paths = []
        status_text = flet.Text()

        def update_target_image_path(e):
            if e.files:
                target_image_path.value = e.files[0].path
                status_text.value = f"Target image uploaded: {os.path.basename(target_image_path.value)}"
                page.update()

        def update_known_image_path(e):
            if e.files:
                known_image_paths.append(e.files[0].path)
                status_text.value = f"Known images uploaded: {', '.join([os.path.basename(path) for path in known_image_paths])}"
                page.update()

        def save_processed_image(e):
            if e.path:
                output_image_path = e.path
                output_dir = os.path.dirname(output_image_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                try:
                    if os.path.exists("temp_processed_image.jpg"):
                        os.replace("temp_processed_image.jpg", output_image_path)
                        if os.path.exists(output_image_path) and os.path.getsize(output_image_path) > 0:
                            status_text.value = f"Processed image saved to: {output_image_path}"
                        else:
                            status_text.value = "Failed to save image."
                    else:
                        status_text.value = "Temporary processed image not found."
                except Exception as ex:
                    status_text.value = f"Error saving image: {str(ex)}"
                page.update()

        def start_processing(e):
            if not target_image_path.value or not known_image_paths:
                page.snack_bar = flet.SnackBar(flet.Text("Please upload all files"))
                page.snack_bar.open = True
                return

            try:
                run_face_recognition_image(
                    target_image_path.value,
                    known_image_paths,
                    "temp_processed_image.jpg",
                )
                status_text.value = "Processing complete! Choose a location to save the image."
                page.snack_bar = flet.SnackBar(flet.Text("Processing complete!"))
                page.snack_bar.open = True

                download_picker.save_file(file_name="processed_image.jpg")
            except Exception as ex:
                status_text.value = f"Error: {str(ex)}"
                page.snack_bar = flet.SnackBar(flet.Text(f"Error: {str(ex)}"))
                page.snack_bar.open = True
            finally:
                page.update()

        page.add(
            flet.Column(
                controls=[
                    flet.ElevatedButton(
                        "Back to Main Page",
                        on_click=go_to_main_page,
                        style=flet.ButtonStyle(
                            bgcolor=flet.Colors.BLUE_700,
                            color=flet.Colors.WHITE,
                            shape=flet.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    flet.Card(
                        content=flet.Container(
                            content=flet.Column(
                                controls=[
                                    flet.Icon(name=flet.Icons.IMAGE, size=40, color=flet.Colors.GREEN_700),
                                    flet.Text("Upload Target Image", size=20, weight=flet.FontWeight.BOLD),
                                    flet.ElevatedButton(
                                        "Upload Target Image",
                                        on_click=lambda _: target_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.GREEN_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    flet.Icon(name=flet.Icons.IMAGE, size=40, color=flet.Colors.BLUE_700),
                                    flet.Text("Upload Known Images", size=20, weight=flet.FontWeight.BOLD),
                                    flet.ElevatedButton(
                                        "Upload Known Images",
                                        on_click=lambda _: known_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.BLUE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    flet.ElevatedButton(
                                        "Start Face Recognition",
                                        on_click=start_processing,
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.ORANGE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    status_text,
                                    flet.ElevatedButton(
                                        "Save Processed Image",
                                        on_click=lambda _: download_picker.save_file(file_name="processed_image.jpg"),
                                        width=200,
                                        height=50,
                                        style=flet.ButtonStyle(
                                            bgcolor=flet.Colors.PURPLE_700,
                                            color=flet.Colors.WHITE,
                                            shape=flet.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                            ),
                            padding=20,
                        ),
                        elevation=10,
                        margin=10,
                    ),
                ],
                spacing=20,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            ),
            target_image_upload,
            known_image_upload,
            download_picker,
        )

    # Webcam Recognition Page

    def webcam_recognition_page():
        lmm_image_upload = flet.FilePicker(on_result=lambda e: update_lmm_image_path(e))
        image_paths = []
        status_text = flet.Text()
        img = flet.Image(width=640, height=480, fit=flet.ImageFit.CONTAIN, visible=False)
        stop_event = threading.Event()

        def update_lmm_image_path(e):
            if e.files:
                image_paths.append(e.files[0].path)
                status_text.value = f"Images uploaded: {', '.join([os.path.basename(path) for path in image_paths])}"
                page.update()

        def start_webcam(_):
            if not image_paths:
                page.snack_bar = flet.SnackBar(flet.Text("Please upload images of faces to recognize."))
                page.snack_bar.open = True
                return

            status_text.value = "Starting webcam..."
            img.src_base64 = ""  # empty base64 string to make no errors
            img.visible = True  #show the image when the webcam starts
            page.update()

            def update_frame(img_base64):
                img.src_base64 = img_base64
                page.update()

            #start the webcam in another thread
            webcam_thread = threading.Thread(
                target=run_face_recognition_webcam,
                args=(image_paths, update_frame, stop_event),
                daemon=True,
            )
            webcam_thread.start()

        def stop_webcam(_):
            stop_event.set()
            status_text.value = "Webcam stopped."
            img.visible = False  #remove the image when the webcam stops
            page.update()

        page.add(
            flet.Row(
                controls=[
                    flet.Column(
                        controls=[
                            flet.ElevatedButton(
                                "Back to Main Page",
                                on_click=go_to_main_page,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.BLUE_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            flet.ElevatedButton(
                                "Upload Images of Faces",
                                on_click=lambda _: lmm_image_upload.pick_files(),
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.ORANGE_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            flet.ElevatedButton(
                                "Start Webcam",
                                on_click=start_webcam,
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.GREEN_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            flet.ElevatedButton(
                                "Stop Webcam",
                                on_click=stop_webcam,
                                width=200,
                                height=50,
                                style=flet.ButtonStyle(
                                    bgcolor=flet.Colors.RED_700,
                                    color=flet.Colors.WHITE,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            status_text,
                        ],
                        spacing=20,
                        alignment=flet.MainAxisAlignment.START,
                        expand=True, 
                    ),
                    # Right side: Webcam video
                    flet.Container(
                        content=img,
                        alignment=flet.alignment.center,
                        expand=True,
                    ),
                ],
                spacing=20,
                expand=True,  # the row takes full height and width of the page
            ),
            lmm_image_upload,
        )

    page.add(first_page)