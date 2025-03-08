import flet as ft
import threading
import os
from face_rec import (
    run_face_recognition_webcam,
    run_face_recognition_video,
    run_face_recognition_image,
)
from utils import get_name_from_filename

def main(page: ft.Page):
    page.title = "Face Recognition App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT  # Light theme

    # Gradient background for all pages
    page.bgcolor = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[ft.Colors.BLUE_100, ft.Colors.PURPLE_100, ft.Colors.PINK_100],
    )

    # ==================================================
    # First Page: Function Selection
    # ==================================================
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
    first_page = ft.Column(
        controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(name=ft.Icons.VIDEOCAM, size=40, color=ft.Colors.BLUE_700),
                            ft.Text("Face Recognition from a Video", size=20, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "Start",
                                on_click=go_to_video_recognition,
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(name=ft.Icons.IMAGE, size=40, color=ft.Colors.GREEN_700),
                            ft.Text("Face Recognition from an Image", size=20, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "Start",
                                on_click=go_to_image_recognition,
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(name=ft.Icons.CAMERA_ALT, size=40, color=ft.Colors.ORANGE_700),
                            ft.Text("Face Recognition from Webcam", size=20, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "Start",
                                on_click=go_to_webcam_recognition,
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.ORANGE_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=10,
                margin=10,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ==================================================
    # Video Recognition Page
    # ==================================================
    def video_recognition_page():
        video_upload = ft.FilePicker(on_result=lambda e: update_video_file_path(e))
        lmm_image_upload = ft.FilePicker(on_result=lambda e: update_lmm_image_path(e))
        download_picker = ft.FilePicker(on_result=lambda e: save_processed_video(e))
        video_file_path = ft.Ref[str]()
        image_paths = []
        progress = ft.ProgressBar(visible=False, value=0, width=400)
        status_text = ft.Text()
        found_names_text = ft.Text(size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)

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
                page.snack_bar = ft.SnackBar(ft.Text("Please upload all files"))
                page.snack_bar.open = True
                return

            progress.visible = True
            status_text.value = "Processing video..."
            found_names_text.value = ""  # Reset found names text
            page.update()

            def update_progress(value):
                progress.value = value
                page.update()

            try:
                run_face_recognition_video(
                    video_file_path.value,
                    image_paths,
                    "temp_processed_video.mp4",  # Temporary file
                    update_progress,
                    update_found_names,  # Pass the callback to update found names
                )
                status_text.value = "Processing complete! Choose a location to save the video."
                page.snack_bar = ft.SnackBar(ft.Text("Processing complete!"))
                page.snack_bar.open = True

                # Open the file picker to choose the download location
                download_picker.save_file(file_name="processed_video.mp4")
            except Exception as ex:
                status_text.value = f"Error: {str(ex)}"
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
                page.snack_bar.open = True
            finally:
                progress.visible = False
                page.update()

        page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Back to Main Page",
                        on_click=go_to_main_page,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(name=ft.Icons.VIDEOCAM, size=40, color=ft.Colors.BLUE_700),
                                    ft.Text("Upload Video", size=20, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton(
                                        "Upload Video",
                                        on_click=lambda _: video_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.BLUE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    ft.Icon(name=ft.Icons.IMAGE, size=40, color=ft.Colors.GREEN_700),
                                    ft.Text("Upload Images of Faces", size=20, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton(
                                        "Upload Images",
                                        on_click=lambda _: lmm_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.GREEN_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "Start Face Recognition",
                                        on_click=start_processing,
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.ORANGE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    progress,
                                    status_text,
                                    found_names_text,  # Display found names here
                                    ft.ElevatedButton(
                                        "Save Processed Video",
                                        on_click=lambda _: download_picker.save_file(file_name="processed_video.mp4"),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.PURPLE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=20,
                        ),
                        elevation=10,
                        margin=10,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            video_upload,
            lmm_image_upload,
            download_picker,
        )

    # ==================================================
    # Image Recognition Page
    # ==================================================
    def image_recognition_page():
        target_image_upload = ft.FilePicker(on_result=lambda e: update_target_image_path(e))
        known_image_upload = ft.FilePicker(on_result=lambda e: update_known_image_path(e))
        download_picker = ft.FilePicker(on_result=lambda e: save_processed_image(e))
        target_image_path = ft.Ref[str]()
        known_image_paths = []
        status_text = ft.Text()

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
                page.snack_bar = ft.SnackBar(ft.Text("Please upload all files"))
                page.snack_bar.open = True
                return

            try:
                run_face_recognition_image(
                    target_image_path.value,
                    known_image_paths,
                    "temp_processed_image.jpg",  # Temporary file
                )
                status_text.value = "Processing complete! Choose a location to save the image."
                page.snack_bar = ft.SnackBar(ft.Text("Processing complete!"))
                page.snack_bar.open = True

                # Open the file picker to choose the download location
                download_picker.save_file(file_name="processed_image.jpg")
            except Exception as ex:
                status_text.value = f"Error: {str(ex)}"
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
                page.snack_bar.open = True
            finally:
                page.update()

        page.add(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Back to Main Page",
                        on_click=go_to_main_page,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(name=ft.Icons.IMAGE, size=40, color=ft.Colors.GREEN_700),
                                    ft.Text("Upload Target Image", size=20, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton(
                                        "Upload Target Image",
                                        on_click=lambda _: target_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.GREEN_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    ft.Icon(name=ft.Icons.IMAGE, size=40, color=ft.Colors.BLUE_700),
                                    ft.Text("Upload Known Images", size=20, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton(
                                        "Upload Known Images",
                                        on_click=lambda _: known_image_upload.pick_files(),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.BLUE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "Start Face Recognition",
                                        on_click=start_processing,
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.ORANGE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                    status_text,
                                    ft.ElevatedButton(
                                        "Save Processed Image",
                                        on_click=lambda _: download_picker.save_file(file_name="processed_image.jpg"),
                                        width=200,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.PURPLE_700,
                                            color=ft.Colors.WHITE,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=20,
                        ),
                        elevation=10,
                        margin=10,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            target_image_upload,
            known_image_upload,
            download_picker,
        )

    # ==================================================
    # Webcam Recognition Page
    # ==================================================
    def webcam_recognition_page():
        lmm_image_upload = ft.FilePicker(on_result=lambda e: update_lmm_image_path(e))
        image_paths = []
        status_text = ft.Text()
        img = ft.Image(width=640, height=480, fit=ft.ImageFit.CONTAIN, visible=False)  # Hide the image initially
        stop_event = threading.Event()

        def update_lmm_image_path(e):
            if e.files:
                image_paths.append(e.files[0].path)
                status_text.value = f"Images uploaded: {', '.join([os.path.basename(path) for path in image_paths])}"
                page.update()

        def start_webcam(_):
            if not image_paths:
                page.snack_bar = ft.SnackBar(ft.Text("Please upload images of faces to recognize."))
                page.snack_bar.open = True
                return

            status_text.value = "Starting webcam..."
            img.src_base64 = ""  # Initialize with an empty base64 string to avoid errors
            img.visible = True  # Show the image when the webcam starts
            page.update()

            def update_frame(img_base64):
                img.src_base64 = img_base64
                page.update()

            # Start the webcam in a separate thread
            webcam_thread = threading.Thread(
                target=run_face_recognition_webcam,
                args=(image_paths, update_frame, stop_event),
                daemon=True,
            )
            webcam_thread.start()

        def stop_webcam(_):
            stop_event.set()
            status_text.value = "Webcam stopped."
            img.visible = False  # Hide the image when the webcam stops
            page.update()

        # Create a split layout with buttons on the left and webcam video on the right
        page.add(
            ft.Row(
                controls=[
                    # Left side: Buttons and controls
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Back to Main Page",
                                on_click=go_to_main_page,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Upload Images of Faces",
                                on_click=lambda _: lmm_image_upload.pick_files(),
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.ORANGE_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Start Webcam",
                                on_click=start_webcam,
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Stop Webcam",
                                on_click=stop_webcam,
                                width=200,
                                height=50,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.RED_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            status_text,
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,  # Allow the column to take up available space
                    ),
                    # Right side: Webcam video
                    ft.Container(
                        content=img,
                        alignment=ft.alignment.center,
                        expand=True,  # Allow the container to take up available space
                    ),
                ],
                spacing=20,
                expand=True,  # Allow the row to take up the full height and width of the page
            ),
            lmm_image_upload,
        )
    # Start with the first page
    page.add(first_page)