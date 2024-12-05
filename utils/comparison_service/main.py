from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import json
from PIL import Image
import imagehash
import numpy as np
from collections import defaultdict

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Глобальная переменная для хранения пути к папке с изображениями
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

    json_path = os.path.join(image_dir, 'hashes.json')
    if os.path.exists(json_path):
        # Если файл существует, предлагаем пользователю выбор
        return templates.TemplateResponse("confirm_hash.html", {"request": request})
    else:
        # Если файла нет, хешируем изображения
        await perform_hashing(image_dir)
        return RedirectResponse("/", status_code=302)

@app.post("/confirm_hash", response_class=HTMLResponse)
async def confirm_hash(request: Request, action: str = Form(...)):
    global image_dir
    if action == "use_existing":
        # Используем существующий файл hashes.json
        return RedirectResponse("/", status_code=302)
    elif action == "rehash":
        # Пересчитываем хеши
        await perform_hashing(image_dir)
        return RedirectResponse("/", status_code=302)
    else:
        # Неверное действие, возвращаем на главную страницу
        return RedirectResponse("/", status_code=302)

async def perform_hashing(image_dir):
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

    # Оптимизированное сравнение хешей
    hash_size = 8  # Размер хеша imagehash (8x8 по умолчанию)
    hash_length = hash_size * hash_size  # Общее количество бит в хеше
    hash_ints = {}
    for filename, hash_str in hashes.items():
        hash_bin = bin(int(hash_str, 16))[2:].zfill(hash_length)
        hash_array = np.array([int(b) for b in hash_bin], dtype=np.uint8)
        hash_ints[filename] = hash_array

    # Устанавливаем порог расстояния Хэмминга на основе заданного процента схожести
    max_distance = hash_length * (1 - similarity / 100)

    # Создаем индекс хешей
    hash_buckets = defaultdict(list)
    prefix_length = 16  # Длина префикса хеша для группировки
    for filename, hash_array in hash_ints.items():
        # Используем первые N бит хеша в качестве ключа
        prefix = ''.join(map(str, hash_array[:prefix_length]))
        hash_buckets[prefix].append((filename, hash_array))

    similar_pairs = []
    # Сравниваем только внутри одной группы
    for bucket in hash_buckets.values():
        for i in range(len(bucket)):
            filename1, hash1 = bucket[i]
            for j in range(i + 1, len(bucket)):
                filename2, hash2 = bucket[j]
                # Вычисляем расстояние Хэмминга
                difference = np.count_nonzero(hash1 != hash2)
                if difference <= max_distance:
                    similarity_percentage = (1 - difference / hash_length) * 100
                    similar_pairs.append({
                        'file1': filename1,
                        'file2': filename2,
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
    await perform_hashing(image_dir)

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
