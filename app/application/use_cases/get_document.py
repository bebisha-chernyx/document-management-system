from fastapi import HTTPException

from app.infrastructure.repositories.sqlite_document_repository import (
    SQLiteDocumentRepository,
)
from app.infrastructure.storage.local_file_storage import LocalFileStorage


class GetDocument:

    def __init__(self):
        self.repository = SQLiteDocumentRepository()
        self.storage = LocalFileStorage()

    def execute(self, filename):

        document = self.repository.find_by_filename(filename)

        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{filename}' not found."
            )

        document_id = document["document_id"]

        file_path = self.storage.get_path(
            f"{document_id}.pdf"
        )

        if not self.storage.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Document file not found in storage."
            )

        return document, file_path