from app import app, db
from datetime import datetime
import os

from app.models import ImageDB

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
                    pass
    db.session.commit()
