from flask import render_template, send_from_directory, send_file
from app import app
import os

from models import Image

@app.route('/')
@app.route('/index')
def index():
    image_reg = Image.all(app.config['IMAGES_FOLDER']);
    return render_template('index.html', title='Home', user='Miguel', images = image_reg)

@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'],filename)
