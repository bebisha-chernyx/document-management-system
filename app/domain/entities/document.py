from datetime import datetime


class Document:

    def __init__(
        self,
        document_id: str,
        filename: str,
        file_size: int,
        file_hash: str,
        created_at: str | None = None,
    ):
        self.document_id = document_id
        self.filename = filename
        self.file_size = file_size
        self.file_hash = file_hash
        self.created_at = created_at or datetime.utcnow().isoformat()