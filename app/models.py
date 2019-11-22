import os
import datetime
from app import db

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
