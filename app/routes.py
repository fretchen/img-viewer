from flask import render_template, send_from_directory, send_file
from app import app
import os

from models import image_reg, Image

@app.route('/')
@app.route('/index')
def index():
    path = app.config['IMAGES_FOLDER'];
    image_reg = [];
    for root, dirs, files in os.walk(app.config['IMAGES_FOLDER']):
        for file in files:
            if file.endswith(".png"):
                rel_path = os.path.relpath(root, app.config['IMAGES_FOLDER']);
                split_path = rel_path.split(os.sep);
                image = Image(os.path.join(rel_path, file), int(split_path[0]),
                    int(split_path[1]), int(split_path[2]));
                image_reg.append(image)

    return render_template('index.html', title='Home', user='Miguel', images = image_reg)

@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'],filename)
