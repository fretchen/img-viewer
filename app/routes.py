from flask import render_template, send_from_directory, send_file, redirect, url_for
from flask import request, flash
from app import app, db
from datetime import datetime
import os

from app.models import ImageDB, User, images_schema
from app.forms import LoginForm
from flask_login import login_required, current_user, logout_user, login_user
import json

@app.route('/')
@app.route('/index')
def index():
    machines = app.config['EXP_NAMES'];
    machine = app.config['EXP_NAMES'][0];

    page = request.args.get('page', 1, type=int);

    images = ImageDB.query.order_by(ImageDB.date_time.desc()).paginate(page, app.config['IMAGES_PER_PAGE'], True);

    image_reg = images.items;
    start_date = image_reg[0].date.strftime('%Y-%m-%d');
    end_date = image_reg[-1].date.strftime('%Y-%m-%d');

    next_url = url_for('index', page=images.next_num) \
        if images.has_next else None
    prev_url = url_for('index', page=images.prev_num) \
            if images.has_prev else None

    im_json = json.dumps(images_schema.dump(image_reg));
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = im_json,
        machines = machines, sel_machine = machine,
        next_url=next_url, prev_url=prev_url);

@app.route('/machine/<name>')
def index_machine(name):
    machines = app.config['EXP_NAMES'];
    page = request.args.get('page', 1, type=int);
    images = ImageDB.query.filter_by(machine=name).order_by(ImageDB.date_time.desc()).\
        paginate(page, app.config['IMAGES_PER_PAGE'], True);
    image_reg = images.items;

    next_url = url_for('index_machine', name=name, page=images.next_num) \
        if images.has_next else None
    prev_url = url_for('index_machine', name=name, page=images.prev_num) \
        if images.has_prev else None


    dates = ImageDB.query.filter_by(machine=name).\
        order_by(ImageDB.date_time.desc()).with_entities(ImageDB.date).all();
    print(dates[-1][0])
    start_date = dates[-1][0].strftime('%Y-%m-%d');
    end_date = dates[0][0].strftime('%Y-%m-%d');
    im_json = json.dumps(images_schema.dump(image_reg));
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = im_json,
        machines = machines, sel_machine = name,
        next_url=next_url, prev_url=prev_url);

@app.route('/today/<name>')
def today_machine(name):
    machines = app.config['EXP_NAMES'];
    today = datetime.date(datetime.today());
    image_reg = ImageDB.query.filter_by(machine=name, date = today).\
        order_by(ImageDB.date_time.desc()).all();

    start_date = datetime.today().strftime('%Y-%m-%d');
    end_date = datetime.today().strftime('%Y-%m-%d');
    im_json = json.dumps(images_schema.dump(image_reg));
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = im_json,
        machines = machines, sel_machine = name);

@app.route('/machine/<name>/dates/<start>/<end>')
def machine_select_dates(name, start, end):
    page = request.args.get('page', 1, type=int);
    machines = app.config['EXP_NAMES']
    start_date = datetime.date(datetime.strptime(start, '%Y-%m-%d'))
    end_date = datetime.date(datetime.strptime(end, '%Y-%m-%d'))

    images = ImageDB.query.filter(ImageDB.machine==name, ImageDB.date<=end_date,
        ImageDB.date>=start_date).order_by(ImageDB.date_time.desc()).\
        paginate(page, app.config['IMAGES_PER_PAGE'], True);
    image_reg = images.items;

    next_url = url_for('machine_select_dates', name=name,
        start = start, end = end, page=images.next_num) \
        if images.has_next else None
    prev_url = url_for('machine_select_dates', name=name,
        start = start, end = end, page=images.prev_num) \
        if images.has_prev else None
    im_json = json.dumps(images_schema.dump(image_reg));
    return render_template('index.html', start_date = start_date,
        end_date = end_date, images = im_json,
        machines = machines, sel_machine = name,
        next_url=next_url, prev_url=prev_url);

@app.route('/cdn/<int:id>')
def custom_static(id):
    image = ImageDB.query.get(id);
    path = image.path;
    filename = os.path.basename(path);
    folder = os.path.dirname(path)
    print(folder);
    return send_from_directory(folder,filename)

@app.route('/refresh_db/')
@login_required
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

# user registration etc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
