# bot/models/zip_model.py


import os
import zipfile
import tempfile
import shutil
from typing import List
import io


class ZipExtractor:
    def __init__(self, zip_bytes: bytes, extension_filter: List[str] = None):
        self.zip_bytes = zip_bytes
        self.extension_filter = extension_filter or []
        self.temp_dir = tempfile.mkdtemp()

    def extract(self):
        zip_path = os.path.join(self.temp_dir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(self.zip_bytes)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

        if self.extension_filter:
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for fname in files:
                    if not any(fname.lower().endswith(ext.lower()) for ext in self.extension_filter):
                        file_path = os.path.join(root, fname)
                        os.remove(file_path)
                for dname in dirs:
                    dir_path = os.path.join(root, dname)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)

        return self.temp_dir

    def cleanup(self):
        shutil.rmtree(self.temp_dir)