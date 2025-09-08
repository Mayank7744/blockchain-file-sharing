import os
import hashlib
import time
from pathlib import Path

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(file_bytes, filename_hint: str):
    sha = hashlib.sha256(file_bytes).hexdigest()
    safe_name = f"{sha[:16]}_{int(time.time())}_{Path(filename_hint).name}"
    storage_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(storage_path, "wb") as f:
        f.write(file_bytes)
    return {
        "filename": filename_hint,
        "storage_path": storage_path,
        "hash": sha,
        "uploader": "user",  # could be replaced with login info
    }
