from pathlib import Path
import shutil


STORAGE_DIR = Path("storage/documents")


class LocalFileStorage:

    def __init__(self):
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, source_file, document_id):
        file_path = STORAGE_DIR / f"{document_id}.pdf"

        with file_path.open("wb") as destination:
            shutil.copyfileobj(source_file, destination)

        return file_path

    def delete(self, file_path):
        path = Path(file_path)

        if path.exists():
            path.unlink()

    def exists(self, file_path):
        return Path(file_path).exists()

    def rename(self, old_path, new_filename):
        new_path = STORAGE_DIR / new_filename
        Path(old_path).rename(new_path)
        return new_path

    def get_path(self, filename):
        return STORAGE_DIR / filename