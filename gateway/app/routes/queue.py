from fastapi import APIRouter, HTTPException, Form, UploadFile, Request, File

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.config import settings

import gridfs

import httpx

import io


router = APIRouter(prefix='/media', tags=["media"])

MONGO_URL = settings.MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["media_db"]

# Async GridFS buckets
video_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="videos")

files_collection = db["files"]


@router.post("/upload")
async def upload(
    request: Request,
    video_file: UploadFile = File(...),
    uploader: str = Form("anonymous")
):
    """
    Forward the request to auth-service with the Authorization header
    """
    current_user_url = "http://auth-service:8000/users/me"

    # Get the Authorization header from the incoming request
    headers = {}
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(current_user_url, headers=headers, timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Auth service not reachable: {exc}"
            )
    if response.status_code == 200:
        # Read uploaded file
        video_bytes = await video_file.read()
        # Save video in GridFS asynchronously
        video_id = await video_bucket.upload_from_stream(video_file.filename, io.BytesIO(video_bytes))
        return response.json()
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail=error_detail,
        )