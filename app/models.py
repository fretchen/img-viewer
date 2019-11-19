import os
import pandas as pd
import datetime
from app import db

class ImageDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), index=True, unique=True)
    machine = db.Column(db.String(64))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)

    def __init__(self, path, machine=[], year = 0, month = 0, day = 0):
        self.path = path;
        self.machine = machine;
        self.year = year;
        self.month = month;
        self.day = day;

    def __repr__(self):
        return '<ImageDB {}>'.format(self.path);

class Image:
    def __init__(self, path, year = 0, month = 0, day = 0):
        self.path = path;
        self.year = year;
        self.month = month;
        self.day = day;

    def to_dict(self):
        return {'path':self.path, 'year': self.year, 'month': self.month,
            'day': self.day, 'date': self.date()}

    def date(self):
        '''
        returns the date of the shot
        '''
        return datetime.date(self.year, self.month, self.day)

    @classmethod
    def all(cls, img_folder):
        """Return a list of files contained in the directory pointed by settings.GALLERY_ROOT_DIR.
        """
        image_reg = [];
        for root, dirs, files in os.walk(img_folder):
            for file in files:
                if file.endswith(".png"):
                    rel_path = os.path.relpath(root, img_folder);
                    split_path = rel_path.split(os.sep);
                    image = cls(os.path.join(rel_path, file), int(split_path[0]),
                        int(split_path[1]), int(split_path[2]));
                    image.date()
                    image_reg.append(image.to_dict())
        df = pd.DataFrame(image_reg);
        return df.sort_values('date', ascending=False)
