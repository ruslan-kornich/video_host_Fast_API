import shutil
from typing import List

from fastapi import UploadFile, File, APIRouter, Form
from fastapi.responses import JSONResponse

from schemas import UploadVideo, GetVideo, Message

video_router = APIRouter()


@video_router.post("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f"{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name ": file.filename, "info": info}


@video_router.post("/img", status_code=201)
async def upload_image(files: List[UploadFile] = File(...)):
    for image in files:
        with open(f"{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    return {"file_name ": "Good"}


@video_router.get("/video", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video():
    user = {"id": 25, "name": "Some Name"}
    video = {"title": "Test", "description": "Description"}
    title = "Test"
    desc = "Description"
    info = GetVideo(user=user, video=video)
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@video_router.get("/test")
async def get_test():
    return JSONResponse(status_code=404, content={"message": "Item not found"})
