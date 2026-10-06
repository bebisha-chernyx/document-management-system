from fastapi import HTTPException

from app.infrastructure.repositories.sqlite_document_repository import (
    SQLiteDocumentRepository,
)
from app.infrastructure.storage.local_file_storage import LocalFileStorage


class DeleteDocument:

    def __init__(self):
        self.repository = SQLiteDocumentRepository()
        self.storage = LocalFileStorage()

    def execute(self, filename):

        # 1. Find document using filename
        document = self.repository.find_by_filename(filename)

        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{filename}' not found."
            )

        # 2. Get internal document ID
        document_id = document["document_id"]

        # 3. Get physical file path
        file_path = self.storage.get_path(
            f"{document_id}.pdf"
        )

        # 4. Delete the PDF
        self.storage.delete(file_path)

        # 5. Delete metadata from SQLite
        self.repository.delete(document_id)

        return filename
    