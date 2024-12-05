from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import json
from PIL import Image
import imagehash

app = FastAPI()

templates = Jinja2Templates(directory="templates")

image_dir = None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global image_dir
    json_exists = False
    if image_dir:
        json_exists = os.path.exists(os.path.join(image_dir, 'hashes.json'))
    return templates.TemplateResponse("index.html", {"request": request, "json_exists": json_exists})

@app.post("/hash", response_class=HTMLResponse)
async def hash_images(request: Request, folder_path: str = Form(...)):
    global image_dir
    image_dir = folder_path

    # Проверяем, существует ли указанный путь и является ли он директорией
    if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
        error_message = "Указанный путь не существует или не является директорией."
        return templates.TemplateResponse("index.html", {"request": request, "error": error_message, "json_exists": False})

    # Хешируем изображения и сохраняем в JSON-файл
    hashes = {}
    for filename in os.listdir(image_dir):
        if filename.lower().endswith('.webp'):
            filepath = os.path.join(image_dir, filename)
            try:
                with Image.open(filepath) as img:
                    hash_value = str(imagehash.average_hash(img))
                    hashes[filename] = hash_value
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")
    # Сохраняем хеши в JSON-файл
    json_path = os.path.join(image_dir, 'hashes.json')
    with open(json_path, 'w') as f:
        json.dump(hashes, f)
    return RedirectResponse("/", status_code=302)

@app.post("/compare", response_class=HTMLResponse)
async def compare_images(request: Request, similarity: int = Form(...)):
    global image_dir
    if not image_dir:
        return RedirectResponse("/", status_code=302)

    json_path = os.path.join(image_dir, 'hashes.json')
    if not os.path.exists(json_path):
        return RedirectResponse("/", status_code=302)

    # Загружаем хеши из JSON-файла
    with open(json_path, 'r') as f:
        hashes = json.load(f)

    # Сравниваем хеши
    similar_pairs = []
    filenames = list(hashes.keys())
    for i in range(len(filenames)):
        for j in range(i+1, len(filenames)):
            hash1 = imagehash.hex_to_hash(hashes[filenames[i]])
            hash2 = imagehash.hex_to_hash(hashes[filenames[j]])
            # Вычисляем процент схожести
            difference = hash1 - hash2  # Hamming distance
            hash_size = hash1.hash.size  # Общее количество бит в хеше
            similarity_percentage = (1 - difference / hash_size) * 100
            if similarity_percentage >= similarity:
                similar_pairs.append({
                    'file1': filenames[i],
                    'file2': filenames[j],
                    'similarity': round(similarity_percentage, 2)
                })
    return templates.TemplateResponse("compare.html", {"request": request, "similar_pairs": similar_pairs})

@app.post("/delete", response_class=HTMLResponse)
async def delete_images(request: Request):
    global image_dir
    if not image_dir:
        return RedirectResponse("/", status_code=302)

    form = await request.form()
    filenames_to_delete = []

    for key in form.keys():
        if key.startswith('delete_'):
            filename = form[key]
            if filename:
                filenames_to_delete.append(filename)

    # Удаляем выбранные файлы
    for filename in filenames_to_delete:
        filepath = os.path.join(image_dir, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Удален файл {filename}")
        except Exception as e:
            print(f"Ошибка при удалении {filename}: {e}")
            continue  # Пропускаем ошибки при удалении файлов

    # Пересчитываем хеши
    hashes = {}
    for filename in os.listdir(image_dir):
        if filename.lower().endswith('.webp'):
            filepath = os.path.join(image_dir, filename)
            try:
                with Image.open(filepath) as img:
                    hash_value = str(imagehash.average_hash(img))
                    hashes[filename] = hash_value
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")
    # Сохраняем обновленные хеши в JSON-файл
    json_path = os.path.join(image_dir, 'hashes.json')
    with open(json_path, 'w') as f:
        json.dump(hashes, f)

    return RedirectResponse("/", status_code=302)

# Эндпоинт для обслуживания изображений
@app.get("/images/{filename}")
async def get_image(filename: str):
    global image_dir
    if not image_dir:
        return "No image directory set"
    file_path = os.path.join(image_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return "File not found"
