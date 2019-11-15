import os

class Image:
    def __init__(self, path, year = 0, month = 0, day = 0):
        self.path = path;
        self.year = year;
        self.month = month;
        self.day = day;

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
                    image_reg.append(image)
        return image_reg;
