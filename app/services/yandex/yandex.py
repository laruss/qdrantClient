import json

import cloudscraper
from bs4 import BeautifulSoup

from app.services.yandex.schemas import UploadContent, SerpItem
from app.utils.logger import logger

URL = 'https://yandex.com/images/search'


def get_similar_images(file_path: str) -> list[SerpItem]:
    files = dict(upfile=('blob', open(file_path, 'rb'), 'image/jpeg'))
    params = dict(rpt='imageview', format='json', request='{"blocks":[{"block":"b-page_type_search-by-image__link"}]}')
    session = cloudscraper.create_scraper()
    response = session.post(URL, params=params, files=files)
    content_data = json.loads(response.content)

    if content_data.get('captcha'):
        raise Exception('Captcha is required, try again later or use VPN.')

    content = UploadContent(**content_data)

    params = content.blocks[0].params
    query_string = params.url
    query_string += f"url=https://avatars.mds.yandex.net/get-images-cbir/{params.cbirId}/orig&cbir_page=similar"
    similar_images_url = URL + '?' + query_string

    response = session.get(similar_images_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('div', class_='serp-item_type_search')

    result_list = []

    for el in elements:
        data_bem = json.loads(el['data-bem'])
        try:
            result_list.append(SerpItem(**data_bem['serp-item']))
        except Exception as e:
            logger.warning(f"Error: {e}")
            logger.warning(f"Data: {data_bem}")

    return result_list
