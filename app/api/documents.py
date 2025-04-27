import json
import os, requests

from fastapi import APIRouter, Path, HTTPException, File, UploadFile

from ..services.s3 import s3_service, DocumentType

documents_router = APIRouter(prefix="/documents", tags=["documents"])

@documents_router.post("/submit")
async def submit_document(
    claim_number_str: str,
    name: str,
    member_id: str,
    group_id: str,
    details: str,
    bill: UploadFile = File(..., description="The file to upload"),
    explanation_of_benefits: UploadFile = File(..., description="The file to upload"),
    policy: UploadFile = File(..., description="The file to upload"),
):
    uploaded_file_ids = {
        name: json.loads(requests.post(
            "https://api.openai.com/v1/files",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            },
            data={
                "purpose": "user_data",
            },
            files={
                "file": f.file,
            },
        ).content)["id"]
        for name, f in (("bill", bill),
                        ("explanation_of_benefits", explanation_of_benefits),
                        ("policy", policy))
    }
    print("DONE")

@documents_router.post("/generate-upload-url/{user_id}/{case_id}/{document_type}")
async def generate_upload_url(
    user_id: str = Path(..., description="User ID"),
    case_id: str = Path(..., description="Case ID"),
    document_type: DocumentType = Path(..., description="Type of document (bill, eob, or policy)"),
    file_name: str = Path(..., description="Name of the file to upload"),
):
    """Generate a presigned URL for direct upload to S3"""
    try:
        result = s3_service.generate_presigned_url(
            user_id=user_id,
            case_id=case_id,
            file_name=file_name,
            document_type=document_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@documents_router.get("/{user_id}/{case_id}/{document_type}/{filename}")
async def get_document_url(
    user_id: str = Path(..., description="User ID"),
    case_id: str = Path(..., description="Case ID"),
    document_type: DocumentType = Path(..., description="Type of document"),
    filename: str = Path(..., description="Name of the file"),
):
    """Get a presigned URL for downloading a document"""
    try:
        file_path = f"{user_id}/{case_id}/{document_type}/{filename}"
        url = s3_service.get_download_url(file_path)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Document not found")
