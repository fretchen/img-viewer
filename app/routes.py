from flask import render_template, send_from_directory, send_file
from app import app
import os
import glob


image_dir = '../../'

@app.route('/')
@app.route('/index')
def index():
    path = app.config['IMAGES_FOLDER'];
    image_names = [];
    images = [];
    rel_paths = []
    for root, dirs, files in os.walk(app.config['IMAGES_FOLDER']):
        for file in files:
            if file.endswith(".png"):
                rel_path = os.path.relpath(root, app.config['IMAGES_FOLDER']);
                split_path = rel_path.split(os.sep);
                images.append({'image_name': os.path.join(rel_path, file),
                'year':int(split_path[0]), 'month':int(split_path[1]),
                'day': int(split_path[2])})
                rel_paths.append(rel_path)

    return render_template('index.html', title='Home', user='Miguel', images = reversed(images))

@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'],filename)
