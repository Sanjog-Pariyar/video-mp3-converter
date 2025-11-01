import io
import tempfile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from moviepy import VideoFileClip
from bson import ObjectId

from app.config import settings
from app.queues.produce import publish_to_queue


# MongoDB setup
MONGO_URL = settings.MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["media_db"]

video_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="videos")
audio_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="audios")


async def convert_video_to_audio(video_file):
    """
    Convert a video (stored in MongoDB GridFS) to MP3 audio
    and save the MP3 back to GridFS.
    """
    try:
        # Step 1: Download video from GridFS
        video_id = ObjectId(video_file['video_fid'])
        download_stream = await video_bucket.open_download_stream(video_id)
        video_bytes = await download_stream.read()
        video_filename = download_stream.filename or "input_video.mp4"

        # Step 2: Write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_bytes)
            temp_video_path = temp_video.name

        # Step 3: Convert video → audio using MoviePy
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio_path = temp_audio.name

        clip = VideoFileClip(temp_video_path)
        clip.audio.write_audiofile(temp_audio_path)
        clip.close()

        # Step 4: Read converted audio bytes
        with open(temp_audio_path, "rb") as f:
            audio_bytes = f.read()

        # Step 5: Upload MP3 to GridFS
        audio_filename = video_filename.rsplit(".", 1)[0] + ".mp3"
        audio_id = await audio_bucket.upload_from_stream(
            audio_filename, io.BytesIO(audio_bytes)
        )

        message = {
            "video_fid": video_file['video_fid'],
            "mp3_fid": str(audio_id),
            "username": video_file["username"],
        }
        print(f"✅ Converted and saved audio as {audio_filename}, message={message}")

        # Step 6: Publish result to RabbitMQ
        publish_to_queue(message)

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
