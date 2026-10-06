from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from app.application.use_cases.upload_document import UploadDocument
from app.application.use_cases.list_documents import ListDocuments
from app.application.use_cases.get_document import GetDocument
from app.application.use_cases.delete_document import DeleteDocument


router = APIRouter()


@router.post("/documents")
def upload(file: UploadFile = File(...)):

    use_case = UploadDocument()

    document = use_case.execute(file)

    return {
        "message": "Document uploaded successfully.",
        "filename": document.filename,
        "file_size": document.file_size,
        "file_hash": document.file_hash,
        "created_at": document.created_at,
    }


@router.get("/documents")
def list_all():

    use_case = ListDocuments()

    return use_case.execute()


@router.get("/documents/{filename}")
def get(filename: str):

    use_case = GetDocument()

    document, file_path = use_case.execute(filename)

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=document["filename"],
    )


@router.delete("/documents/{filename}")
def delete(filename: str):

    use_case = DeleteDocument()

    use_case.execute(filename)

    return {
        "message": "Document deleted successfully.",
        "filename": filename,
    }