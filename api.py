import shutil

from fastapi import UploadFile, File, APIRouter, Form

from models import Video, User
from schemas import UploadVideo, Message, GetVideo

video_router = APIRouter()


@video_router.post("/")
async def create_video(
        title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)
):
    info = UploadVideo(title=title, description=description)
    with open(f"{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=file.filename, user=user, **info.dict())


@video_router.get("/video/{video_pk}", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related("user").get(pk=video_pk)
