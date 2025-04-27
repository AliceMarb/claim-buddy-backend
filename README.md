# ClaimBuddy Backend

A FastAPI backend service for managing medical claims and related documents.

## Setup

1. Create a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET_NAME=your_bucket
DATABASE_URL=your_dynamo_or_db_url
OPENAI_API_KEY=your_openai_key
FRONTEND_ORIGIN=https://yourfrontend.vercel.app
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Health Check
- `GET /health` - Check API health
- `GET /ping` - Simple ping endpoint

### Document Management

#### Generate Upload URL
```http
POST /documents/generate-upload-url/{user_id}/{case_id}/{document_type}?file_name={filename}
```
Generates a presigned URL for direct upload to S3.

Parameters:
- `user_id`: User identifier
- `case_id`: Case identifier
- `document_type`: Type of document (`bill`, `eob`, or `policy`)
- `file_name`: Name of the file to upload

Response:
```json
{
    "url": "presigned-s3-upload-url",
    "key": "user_id/case_id/document_type/filename"
}
```

#### Get Document Download URL
```http
GET /documents/{user_id}/{case_id}/{document_type}/{filename}
```
Generates a presigned URL for downloading a document.

Parameters:
- `user_id`: User identifier
- `case_id`: Case identifier
- `document_type`: Type of document (`bill`, `eob`, or `policy`)
- `filename`: Name of the file

Response:
```json
{
    "url": "presigned-s3-download-url"
}
```

## File Storage Structure

Documents are stored in S3 with the following structure:
```
/userId/caseId/bill/filename.pdf
/userId/caseId/eob/filename.pdf
/userId/caseId/policy/filename.pdf
```

## Frontend Integration Example

```javascript
// 1. Get the presigned URL for upload
const response = await fetch(
    '/api/documents/generate-upload-url/user123/case456/bill?file_name=invoice.pdf'
);
const { url, key } = await response.json();

// 2. Upload file directly to S3
await fetch(url, {
    method: 'PUT',
    body: fileData,
    headers: {
        'Content-Type': 'application/octet-stream'
    }
});

// 3. Get download URL for the file
const downloadResponse = await fetch(
    '/api/documents/user123/case456/bill/invoice.pdf'
);
const { url: downloadUrl } = await downloadResponse.json();
```

## Development

- API documentation available at `/docs` or `/redoc`
- Uses FastAPI for high-performance async API
- Direct S3 uploads using presigned URLs
- CORS enabled for frontend integration
