from flask import Flask
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

app = Flask(__name__);
app.config.from_object(Config);
db = SQLAlchemy(app);
migrate = Migrate(app, db);
ma = Marshmallow(app);

login = LoginManager(app);
login.login_view = 'login';

if not os.path.exists('logs'):
        os.mkdir('logs')
file_handler = RotatingFileHandler('logs/imgviewer.log', maxBytes=10240,
                                       backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

from app import routes
