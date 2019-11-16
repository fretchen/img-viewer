import os

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # config of the camera stuff
    EXP_NAMES = [key for key in config['IMAGE_FOLDERS']];
    IMAGE_FOLDERS = [];
    for key in config['IMAGE_FOLDERS']:
        path = config['IMAGE_FOLDERS'][key];
        print(path)
        print(os.path.exists(path))
        if os.path.exists(path):
            IMAGE_FOLDERS.append(os.path.abspath(path))
        elif os.path.exists(os.path.join(basedir, path)):
            IMAGE_FOLDERS.append(os.path.join(basedir, config['IMAGE_FOLDERS'][key]));
