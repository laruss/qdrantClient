import os
import shutil
import tempfile
from PIL import Image, ImageChops
import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app
import json

@pytest.fixture(scope="module")
def temp_image_dir():
    # Создаём временную директорию для тестов
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Удаляем временную директорию после тестов
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="module")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c

def create_image(path, color, size=(100, 100)):
    img = Image.new('RGB', size, color=color)
    img.save(path, format='WEBP')

def create_similar_image(original_path, new_path, delta):
    with Image.open(original_path) as img:
        # Вносим небольшие изменения в изображение
        delta_img = Image.new('RGB', img.size, color=delta)
        img = ImageChops.add(img, delta_img)
        img.save(new_path, format='WEBP')

@pytest.mark.asyncio
async def test_hash_and_compare(client, temp_image_dir):
    # Создаём два идентичных изображения
    image1_path = os.path.join(temp_image_dir, 'image1.webp')
    image2_path = os.path.join(temp_image_dir, 'image2.webp')
    create_image(image1_path, color='red')
    shutil.copy(image1_path, image2_path)

    # Создаём третье изображение с небольшими изменениями
    image3_path = os.path.join(temp_image_dir, 'image3.webp')
    create_similar_image(image1_path, image3_path, delta=(10, 0, 0))

    # Создаём четвёртое совершенно другое изображение
    image4_path = os.path.join(temp_image_dir, 'image4.webp')
    create_image(image4_path, color='blue')

    # Тестируем хеширование изображений
    response = await client.post("/hash", data={"folder_path": temp_image_dir})
    assert response.status_code == 200 or response.status_code == 302
    assert os.path.exists(os.path.join(temp_image_dir, 'hashes.json'))

    # Тестируем сравнение с 100% схожестью (должны найти идентичные изображения)
    response = await client.post("/compare", data={"similarity": 100})
    assert response.status_code == 200
    content = response.text
    assert 'image1.webp' in content
    assert 'image2.webp' in content
    # Проверяем, что пара image1.webp и image2.webp найдена
    assert content.count('image1.webp') >= 1
    assert content.count('image2.webp') >= 1

    # Тестируем сравнение с 0% схожестью (должны быть найдены все пары)
    response = await client.post("/compare", data={"similarity": 0})
    assert response.status_code == 200
    content = response.text
    # Проверяем, что есть результаты
    assert 'Похожие изображения' in content

    # Тестируем удаление изображений
    # Выбираем удалить image2.webp
    data = {
        'delete_1': 'image2.webp',  # Индекс соответствует порядку в шаблоне
        'delete_2': '',  # Не удалять
        'delete_3': '',  # Не удалять
    }
    response = await client.post("/delete", data=data)
    assert response.status_code == 200 or response.status_code == 302
    assert not os.path.exists(image2_path)
    # Проверяем, что хеши пересчитаны
    with open(os.path.join(temp_image_dir, 'hashes.json'), 'r') as f:
        hashes = json.load(f)
    assert 'image2.webp' not in hashes

    # Тестируем повторное сравнение после удаления
    response = await client.post("/compare", data={"similarity": 100})
    assert response.status_code == 200
    content = response.text
    # Проверяем, что image2.webp больше нет в результатах
    assert 'image2.webp' not in content

    # Тестируем указание одной и той же картинки дважды
    # Создаём дубликат image1.webp
    duplicate_image_path = os.path.join(temp_image_dir, 'duplicate.webp')
    shutil.copy(image1_path, duplicate_image_path)
    # Перехешируем изображения
    response = await client.post("/hash", data={"folder_path": temp_image_dir})
    assert response.status_code == 200 or response.status_code == 302
    # Сравниваем с 100% схожестью
    response = await client.post("/compare", data={"similarity": 100})
    assert response.status_code == 200
    content = response.text
    # Проверяем, что дубликаты найдены
    assert 'duplicate.webp' in content
    assert content.count('image1.webp') >= 1
    assert content.count('duplicate.webp') >= 1

    # Тестируем граничные значения схожести
    # Сравнение с 0% схожестью
    response = await client.post("/compare", data={"similarity": 0})
    assert response.status_code == 200
    content = response.text
    assert 'Похожие изображения' in content

@pytest.mark.asyncio
async def test_invalid_path(client):
    # Тестируем поведение при неверном пути
    invalid_path = "/invalid/path"
    response = await client.post("/hash", data={"folder_path": invalid_path})
    assert response.status_code == 200
    # Проверяем, что приложение вернуло сообщение об ошибке
    assert "Указанный путь не существует или не является директорией." in response.text

@pytest.mark.asyncio
async def test_no_images(client, temp_image_dir):
    # Тестируем поведение при отсутствии изображений в папке
    # Удаляем все изображения из папки
    for filename in os.listdir(temp_image_dir):
        os.remove(os.path.join(temp_image_dir, filename))
    response = await client.post("/hash", data={"folder_path": temp_image_dir})
    assert response.status_code == 200 or response.status_code == 302
    # Проверяем, что файл hashes.json создан и пуст
    hashes_path = os.path.join(temp_image_dir, 'hashes.json')
    assert os.path.exists(hashes_path)
    with open(hashes_path, 'r') as f:
        hashes = json.load(f)
    assert len(hashes) == 0
