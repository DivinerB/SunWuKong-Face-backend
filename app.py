from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pathlib import Path
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from face_swap import face_swap
IMAGES_DIR = Path("./result_uploads")

@app.post("/face-swap")
async def create_upload_file(avatar: UploadFile):
  file_location = f"uploads/{avatar.filename}"
  with open(file_location, "wb+") as file_object:
      file_object.write(avatar.file.read())
  new_file_location = face_swap(file_location)
  print(new_file_location)
  return {"result": new_file_location}

@app.get("/result_uploads/{filename}")
async def stream_image(filename: str):
    file_path = IMAGES_DIR / filename
    if file_path.exists() and file_path.is_file():
        # Open the file and stream it
        with open(file_path, "rb") as file:
            return StreamingResponse(io.BytesIO(file.read()), media_type="image/jpeg")
    return {"error": "File not found"}
