import os
from dotenv import load_dotenv

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
#print(config['IMAGE_FOLDERS'])
for key in config['IMAGE_FOLDERS']:
    print(key + '/' + config['IMAGE_FOLDERS'][key])
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'amTestKey'

    # config of the camera stuff
    IMAGES_FOLDER = os.environ.get('IMAGES_FOLDER') or os.path.join(basedir, 'Images');
    EXP_NAMES = [key for key in config['IMAGE_FOLDERS']];
    IMAGE_FOLDERS = [config['IMAGE_FOLDERS'][key] for key in config['IMAGE_FOLDERS']];
