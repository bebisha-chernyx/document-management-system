from app.infrastructure.repositories.sqlite_document_repository import (
    SQLiteDocumentRepository,
)


class ListDocuments:

    def __init__(self):
        self.repository = SQLiteDocumentRepository()

    def execute(self):

        documents = self.repository.find_all()

        return [
            {
                "filename": document["filename"],
                "file_size": document["file_size"],
                "file_hash": document["file_hash"],
                "created_at": document["created_at"],
            }
            for document in documents
        ]