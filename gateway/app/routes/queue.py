from fastapi import APIRouter, HTTPException, Form, UploadFile, Request, File

import tempfile

from fastapi.responses import StreamingResponse

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.config import settings

import gridfs
import httpx
import io
import json
from bson import ObjectId


from app.queue.produce import publish_to_queue


router = APIRouter(prefix='/media', tags=["media"])

MONGO_URL = settings.MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["media_db"]

# Async GridFS buckets
video_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="videos")
audio_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="audios")

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
        user_details = response.json()
        message = {
            "video_fid": str(video_id),
            "mp3_fid": None,
            "username": user_details["email"]
        }
        publish_to_queue(message)
        return message
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail=error_detail,
        )

@router.get("/download")
async def download(request: Request, mp3_fid: str):
    """
    Authenticates via auth-service, then streams audio (MP3) from MongoDB GridFS directly.
    """
    current_user_url = "http://auth-service:8000/users/me"

    # Forward Authorization header
    headers = {}
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    # Validate user
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(current_user_url, headers=headers, timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Auth service not reachable: {exc}")

    if response.status_code != 200:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    # ---- Authenticated, stream file ----
    try:
        audio_id = ObjectId(mp3_fid)
        download_stream = await audio_bucket.open_download_stream(audio_id)
        audio_filename = download_stream.filename or "converted_audio.mp3"

        async def file_iterator():
            """Stream chunks asynchronously from GridFS."""
            chunk_size = 8192
            while True:
                chunk = await download_stream.readchunk()
                if not chunk:
                    break
                yield chunk

        headers = {
            "Content-Disposition": f'attachment; filename="{audio_filename}"'
        }

        return StreamingResponse(
            file_iterator(),
            media_type="audio/mpeg",
            headers=headers
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming file: {e}")