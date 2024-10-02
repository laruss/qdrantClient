import os

import environ

env_ = environ.Env()
environ.Env.read_env()


class Env:
    APP_NAME = env_('APP_NAME')
    APP_VERSION = env_('APP_VERSION')
    QDRANT_HOST = env_('QDRANT_HOST')
    QDRANT_PORT = env_('QDRANT_PORT')
    QDRANT_COLLECTION = env_('QDRANT_COLLECTION')

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

    FACEFUSION_PATH = env_('FACEFUSION_PATH')

    #   set the command to merge the face image and the DO image.
    #   use formatting as {face_image}, {do_image}, {facefusion_path}, {merged_image}
    CLI_MERGE_FACE_COMMAND = '''
conda activate facefusion
cd "{facefusion_path}"
python facefusion.py headless-run -s "{face_image}" -t "{do_image}" --processors face_swapper face_enhancer -o "{merged_image}"
'''


env = Env()
