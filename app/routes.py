from flask import render_template, send_from_directory, send_file, redirect, url_for
from app import app, db
from datetime import datetime
import os

from app.models import Image, ImageDB

@app.route('/')
@app.route('/index')
def index():
    machines = app.config['EXP_NAMES']

    folder = app.config['IMAGE_FOLDERS'][1];
    machine = app.config['EXP_NAMES'][1];
    image_reg = ImageDB.query.order_by(ImageDB.date.desc()).paginate(1, 100, True).items;
    start_date = image_reg[0].date.strftime('%Y-%m-%d');
    end_date = image_reg[-1].date.strftime('%Y-%m-%d');
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

@app.route('/cdn/<int:id>')
def custom_static(id):
    image = ImageDB.query.get(id);
    path = image.path;
    filename = os.path.basename(path);
    folder = os.path.dirname(path)
    print(folder);
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
    machines = app.config['EXP_NAMES'];
    today = datetime.date(datetime.today());

    if name in machines:
            for ii, key in enumerate(machines):
                if key == name:
                    folder = app.config['IMAGE_FOLDERS'][ii];
    else:
        return redirect(url_for('index'))

    image_reg = Image.all(folder);
    mask = image_reg['date'] == today;
    image_reg = image_reg.loc[mask];

    start_date = datetime.today().strftime('%Y-%m-%d');
    end_date = datetime.today().strftime('%Y-%m-%d');
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = image_reg,
        machines = machines, sel_machine = name);

@app.route('/refresh_db/')
def add_images():
    '''
    we need to fill up the data base at some point.
    '''
    machines = app.config['EXP_NAMES'];
    for ii, key in enumerate(machines):
        img_folder = app.config['IMAGE_FOLDERS'][ii];
        for root, dirs, files in os.walk(img_folder):
            for file in files:
                if file.endswith(".png"):
                    rel_path = os.path.relpath(root, img_folder);
                    full_path = os.path.join(root, file);
                    old_image = ImageDB.query.filter_by(path = full_path).first();
                    if not old_image:
                        split_path = rel_path.split(os.sep);

                        image = ImageDB(path = full_path, machine = key,
                            year = int(split_path[0]), month = int(split_path[1]),
                            day = int(split_path[2]))
                        db.session.add(image)
                        print('Added ' + full_path)
                    else:
                        print('Ignored ' + full_path)
                        pass
        db.session.commit()

    return redirect(url_for('index'))
