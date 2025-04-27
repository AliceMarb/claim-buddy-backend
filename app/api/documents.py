from fastapi import APIRouter, Path, HTTPException
from ..services.s3 import s3_service, DocumentType

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/generate-upload-url/{user_id}/{case_id}/{document_type}")
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

@router.get("/{user_id}/{case_id}/{document_type}/{filename}")
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