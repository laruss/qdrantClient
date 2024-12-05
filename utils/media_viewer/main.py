from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

media_path = None
images_list = []
current_index = 0
mode = "random"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/set_media_path")
async def set_media_path(request: Request):
    form = await request.form()
    path = form.get("media_path")

    if not os.path.exists(path) or not os.path.isdir(path):
        return JSONResponse({"error": "Путь не существует или не является папкой."}, status_code=400)

    global media_path, images_list, current_index
    media_path = path
    images_list = [f for f in os.listdir(media_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not images_list:
        return JSONResponse({"error": "В каталоге нет медиа-данных."}, status_code=400)

    current_index = random.randint(0, len(images_list) - 1)
    return {"message": "Путь установлен."}


@app.get("/viewer", response_class=HTMLResponse)
async def viewer(request: Request):
    if not media_path or not images_list:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Сначала установите путь к медиа."})
    return templates.TemplateResponse("viewer.html", {"request": request})


@app.get("/get_image")
async def get_image():
    if not images_list:
        return JSONResponse({"error": "Нет изображений."}, status_code=400)

    global current_index

    image_file = images_list[current_index]
    return {"image_url": f"/image/{image_file}"}


@app.get("/image/{filename}")
async def image(filename: str):
    file_path = os.path.join(media_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse({"error": "Файл не найден."}, status_code=404)


@app.post("/change_mode")
async def change_mode():
    global mode
    mode = "random" if mode == "sequential" else "sequential"
    return {"mode": mode}


@app.post("/next_image")
async def next_image():
    global current_index
    if mode == "random":
        current_index = random.randint(0, len(images_list) - 1)
    else:
        current_index = (current_index + 1) % len(images_list)
    return {"message": "Следующее изображение."}


@app.post("/prev_image")
async def prev_image():
    global current_index
    if mode == "random":
        current_index = random.randint(0, len(images_list) - 1)
    else:
        current_index = (current_index - 1) % len(images_list)
    return {"message": "Предыдущее изображение."}
