import os
import zipfile

def zip_processed_images(filepaths, zip_name):
    zip_path = os.path.join("processed", zip_name)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for filepath in filepaths:
            arcname = os.path.basename(filepath)
            zipf.write(filepath, arcname)
    return zip_path
