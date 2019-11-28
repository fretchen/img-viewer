import os
import datetime
from app import db, login, ma

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

class ImageDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), index=True, unique=True)
    machine = db.Column(db.String(64))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, path, machine=[], year = 0, month = 0, day = 0):
        self.path = path;
        self.machine = machine;
        self.year = year;
        self.month = month;
        self.day = day;
        self.date = datetime.date(self.year, self.month, self.day);

    def __repr__(self):
        return '<ImageDB {}>'.format(self.path);

    def to_dict(self):
        return {'id': self.id, 'path': self.path, 'day': self.day,
         'month': self.month, 'year': self.year};

    def to_json(self):
        return image_schema.dumps(self);

class ImageSchema(ma.ModelSchema):
    class Meta:
        model = ImageDB

image_schema = ImageSchema()
images_schema = ImageSchema(many=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
