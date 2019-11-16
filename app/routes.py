from flask import render_template, send_from_directory, send_file
from app import app
from datetime import datetime
import os

from app.models import Image

@app.route('/')
@app.route('/index')
def index():
    image_reg = Image.all(app.config['IMAGES_FOLDER']);
    start_date = image_reg['date'].min().strftime('%Y-%m-%d');
    end_date = image_reg['date'].max().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg)

@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'],filename)

@app.route('/dates/<start>/<end>')
def select_dates(start, end):
    start_date = datetime.date(datetime.strptime(start, '%Y-%m-%d'))
    end_date = datetime.date(datetime.strptime(end, '%Y-%m-%d'))

    image_reg = Image.all(app.config['IMAGES_FOLDER']);
    mask = (image_reg['date'] >= start_date) & (image_reg['date'] <= end_date)
    image_reg = image_reg.loc[mask]
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg)


@app.route('/today/')
def today():
    image_reg = Image.all(app.config['IMAGES_FOLDER']);
    mask = image_reg['date'] == datetime.today();
    image_reg = image_reg.loc[mask];

    start_date = datetime.today().strftime('%Y-%m-%d');
    end_date = datetime.today().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg)
