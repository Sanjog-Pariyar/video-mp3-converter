from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from moviepy import VideoFileClip
import os
import uuid

from app.api import users, login

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://gateway:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(login.router)

@app.get("/")
def get_root():
    return {"message": "Hello world"}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/convert")
async def convert_to_mp3(video_file: UploadFile = File(...)):
    # Temporary unique filenames
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{video_file.filename}")
    output_path = os.path.splitext(input_path)[0] + ".mp3"

    # Save uploaded video temporarily
    with open(input_path, "wb") as f:
        f.write(await video_file.read())

    # Convert video to audio
    clip = VideoFileClip(input_path)
    clip.audio.write_audiofile(output_path)
    clip.close()

    # Optional: remove the video file after conversion
    # os.remove(input_path)

    # Return the MP3 file
    return FileResponse(
        path=output_path,
        filename=f"{os.path.splitext(video_file.filename)[0]}.mp3",
        media_type="audio/mpeg"
    )
