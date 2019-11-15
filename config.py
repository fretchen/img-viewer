import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'amTestKey'

    # config of the camera stuff
    IMAGES_FOLDER = os.environ.get('IMAGES_FOLDER') or os.path.join(basedir, 'Images');
