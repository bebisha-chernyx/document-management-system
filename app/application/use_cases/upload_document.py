from uuid import uuid4

from fastapi import HTTPException

from app.domain.entities.document import Document
from app.infrastructure.repositories.sqlite_document_repository import (
    SQLiteDocumentRepository,
)
from app.infrastructure.storage.local_file_storage import LocalFileStorage
from app.infrastructure.hash.sha256_hash_service import SHA256HashService


MAX_FILE_SIZE = 5 * 1024 * 1024


class UploadDocument:

    def __init__(self):
        self.repository = SQLiteDocumentRepository()
        self.storage = LocalFileStorage()
        self.hash_service = SHA256HashService()

    def execute(self, file):

        # 1. Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        # 2. Validate filename
        filename = file.filename

        if not filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is required."
            )

        # 3. Check duplicate filename
        existing_filename = self.repository.find_by_filename(filename)

        if existing_filename:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"A document named '{filename}' already exists. "
                    "Please choose a different filename."
                )
            )

        # 4. Generate internal document ID
        document_id = str(uuid4())

        # 5. Save file temporarily
        temporary_path = self.storage.save(
            file.file,
            f"{document_id}_temp"
        )

        # 6. Check file size
        file_size = temporary_path.stat().st_size

        if file_size > MAX_FILE_SIZE:
            self.storage.delete(temporary_path)

            raise HTTPException(
                status_code=400,
                detail="File size must not exceed 5 MB."
            )

        # 7. Calculate SHA-256 hash
        file_hash = self.hash_service.calculate(temporary_path)

        # 8. Check duplicate content
        existing_document = self.repository.find_by_hash(file_hash)

        if existing_document:
            self.storage.delete(temporary_path)

            raise HTTPException(
                status_code=409,
                detail="Duplicate document already exists."
            )

        # 9. Rename temporary file to permanent file
        final_path = self.storage.rename(
            temporary_path,
            f"{document_id}.pdf"
        )

        # 10. Create Document entity
        document = Document(
            document_id=document_id,
            filename=filename,
            file_size=file_size,
            file_hash=file_hash,
        )

        # 11. Save metadata
        self.repository.save(document)

        return document
    