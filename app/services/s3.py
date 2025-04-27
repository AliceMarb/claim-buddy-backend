import os
import boto3
from enum import Enum
from typing import Dict, Any

class DocumentType(str, Enum):
    BILL = "bill"
    EOB = "eob"
    POLICY = "policy"

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    def generate_presigned_url(
        self,
        user_id: str,
        case_id: str,
        file_name: str,
        document_type: DocumentType,
        expires_in: int = 300
    ) -> Dict[str, str]:
        """
        Generate a presigned URL for direct upload to S3
        """
        key = f"{user_id}/{case_id}/{document_type}/{file_name}"

        try:
            presigned_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                    "ContentType": "application/octet-stream",
                },
                ExpiresIn=expires_in  # URL expires in 5 minutes
            )
            return {"url": presigned_url, "key": key}
        except Exception as e:
            raise Exception(f"Error generating presigned URL: {str(e)}")

    def get_download_url(self, file_path: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for downloading a file
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            raise Exception(f"Error generating download URL: {str(e)}")

# Create a singleton instance
s3_service = S3Service()