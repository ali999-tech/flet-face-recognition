import os

def get_name_from_filename(image_path):
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    return name