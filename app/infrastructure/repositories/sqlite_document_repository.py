from app.domain.repositories.document_repository import DocumentRepository
from app.infrastructure.database.sqlite import get_connection


class SQLiteDocumentRepository(DocumentRepository):

    def save(self, document):

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO documents
            (
                document_id,
                filename,
                file_size,
                file_hash,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document.document_id,
                document.filename,
                document.file_size,
                document.file_hash,
                document.created_at,
            ),
        )

        connection.commit()
        connection.close()

    def find_by_filename(self, filename):

        connection = get_connection()

        row = connection.execute(
            """
            SELECT *
            FROM documents
            WHERE filename = ?
            """,
            (filename,),
        ).fetchone()

        connection.close()

        return row

    def find_by_hash(self, file_hash):

        connection = get_connection()

        row = connection.execute(
            """
            SELECT *
            FROM documents
            WHERE file_hash = ?
            """,
            (file_hash,),
        ).fetchone()

        connection.close()

        return row

    def find_all(self):

        connection = get_connection()

        rows = connection.execute(
            """
            SELECT *
            FROM documents
            """
        ).fetchall()

        connection.close()

        return rows

    def delete(self, document_id):

        connection = get_connection()

        connection.execute(
            """
            DELETE FROM documents
            WHERE document_id = ?
            """,
            (document_id,),
        )

        connection.commit()
        connection.close()