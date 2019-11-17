from flask import render_template, send_from_directory, send_file, redirect
from app import app
from datetime import datetime
import os

from app.models import Image

@app.route('/')
@app.route('/index')
def index():
    machines = app.config['EXP_NAMES']

    folder = app.config['IMAGE_FOLDERS'][1];
    machine = app.config['EXP_NAMES'][1];

    image_reg = Image.all(folder);

    start_date = image_reg['date'].min().strftime('%Y-%m-%d');
    end_date = image_reg['date'].max().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg,
        machines = machines, sel_machine = machine);

@app.route('/machine/<name>')
def index_machine(name):
    machines = app.config['EXP_NAMES']

    if name in machines:
        for ii, key in enumerate(machines):
            if key == name:
                folder = app.config['IMAGE_FOLDERS'][ii];
    else:
        return redirect(url_for('index'))

    image_reg = Image.all(folder);

    start_date = image_reg['date'].min().strftime('%Y-%m-%d');
    end_date = image_reg['date'].max().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg,
        machines = machines, sel_machine = name);

@app.route('/cdn/<name>/<path:filename>')
def custom_static(name, filename):
    machines = app.config['EXP_NAMES'];
    if name in machines:
        for ii, key in enumerate(machines):
            if key == name:
                folder = app.config['IMAGE_FOLDERS'][ii];
    else:
        return False
    return send_from_directory(folder,filename)

@app.route('/machine/<name>/dates/<start>/<end>')
def machine_select_dates(name, start, end):
    machines = app.config['EXP_NAMES']

    if name in machines:
        for ii, key in enumerate(machines):
            if key == name:
                folder = app.config['IMAGE_FOLDERS'][ii];
    else:
        return redirect(url_for('index'))
    image_reg = Image.all(folder);

    start_date = datetime.date(datetime.strptime(start, '%Y-%m-%d'))
    end_date = datetime.date(datetime.strptime(end, '%Y-%m-%d'))

    mask = (image_reg['date'] >= start_date) & (image_reg['date'] <= end_date)
    image_reg = image_reg.loc[mask]
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg,
        machines = machines, sel_machine = name);

@app.route('/today/<name>')
def today_machine(name):
    machines = app.config['EXP_NAMES']

    if name in machines:
            for ii, key in enumerate(machines):
                if key == name:
                    folder = app.config['IMAGE_FOLDERS'][ii];
    else:
        return redirect(url_for('index'))

    image_reg = Image.all(folder);
    mask = image_reg['date'] == datetime.today();
    image_reg = image_reg.loc[mask];

    start_date = datetime.today().strftime('%Y-%m-%d');
    end_date = datetime.today().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg,
        machines = machines, sel_machine = name);
