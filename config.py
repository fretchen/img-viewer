import os

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # secret key
    if 'SECRET_KEY' in config['DEFAULT']:
        SECRET_KEY = config['DEFAULT']['SECRET_KEY'];
    else:
        SECRET_KEY = 'aTestKey';

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if 'IMAGES_PER_PAGE' in config['DEFAULT']:
        IMAGES_PER_PAGE = int(config['DEFAULT']['IMAGES_PER_PAGE']);
    else:
            IMAGES_PER_PAGE = 25;

    # config of the camera stuff
    EXP_NAMES = [];
    IMAGE_FOLDERS = [];
    for key in config['IMAGE_FOLDERS']:
        path = config['IMAGE_FOLDERS'][key];
        if os.path.exists(path):
            IMAGE_FOLDERS.append(os.path.abspath(path));
            EXP_NAMES.append(key);
        elif os.path.exists(os.path.join(basedir, path)):
            IMAGE_FOLDERS.append(os.path.join(basedir, config['IMAGE_FOLDERS'][key]));
            EXP_NAMES.append(key);
