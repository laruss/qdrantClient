import os

import environ

env_ = environ.Env()
environ.Env.read_env()


with open('anthropic_prompt.txt', 'r') as file:
    ANTHROPIC_PROMPT = file.read()


class Env:
    APP_NAME = env_('APP_NAME')
    APP_VERSION = env_('APP_VERSION')
    QDRANT_HOST = env_('QDRANT_HOST')
    QDRANT_PORT = env_('QDRANT_PORT')
    QDRANT_COLLECTION = env_('QDRANT_COLLECTION')

    MONGODB_USER = env_('MONGODB_USER')
    MONGODB_PASSWORD = env_('MONGODB_PASSWORD')
    MONGODB_DB_NAME = env_('MONGODB_DB_NAME')
    MONGODB_HOST = env_('MONGODB_HOST')
    MONGODB_PORT = env_('MONGODB_PORT')
    MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}"

    DOP_SPACE_PRIVATE_API_KEY = env_('DOP_SPACE_PRIVATE_API_KEY')
    DOP_SPACE_PUBLIC_ACCESS_KEY = env_('DOP_SPACE_PUBLIC_ACCESS_KEY')
    DOP_SPACE_NAME = env_('DOP_SPACE_NAME')
    DOP_SPACE_REGION = env_('DOP_SPACE_REGION')
    DOP_PATH = "media/"

    BASE_DIR, _ = os.path.split(os.path.abspath(__file__))
    TEMP_DIR = BASE_DIR + '/tmp/'
    FACE_IMAGE_PATH = TEMP_DIR + 'face_image.png'
    DO_IMAGE_PATH = TEMP_DIR + 'do_image.png'
    MERGED_IMAGE_PATH = TEMP_DIR + 'merged_image.png'
    TEMP_DUPLICATES_PATH = TEMP_DIR + 'duplicates/'
    TEMP_LOOK_ALIKES_PATH = TEMP_DIR + 'look_alikes/'

    ANTHROPIC_API_KEY = env_('ANTHROPIC_API_KEY')
    ANTHROPIC_PROMPT = ANTHROPIC_PROMPT

    API_PREFIX = os.getenv('API_PREFIX', '')

    FACEFUSION_PATH = env_('FACEFUSION_PATH')

    #   set the command to merge the face image and the DO image.
    #   use formatting as {face_image}, {do_image}, {facefusion_path}, {merged_image}
    CLI_MERGE_FACE_COMMAND = '''
conda activate facefusion
cd "{facefusion_path}"
python facefusion.py headless-run -s "{face_image}" -t "{do_image}" --processors face_swapper face_enhancer -o "{merged_image}"
'''


env = Env()
