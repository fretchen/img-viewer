# PI-viewer

 Look into the shots we took with labscriptsuite. It is a great way to keep the
 larger public like the PI in the loop on what is going on in the lab. The software
 stack is really just [flask](https://palletsprojects.com/p/flask/) with some gimmicks around it.

 While this program can be installed on your personal PC
 for dev purposes it is not super useful there as we typically have easily thousands and thousands of images to
 crawl through. So this project is typically really designed to run on a public server.
 This also comes with quite a bit of tools around the core functionality that we
 need to implement to secure it like servers, login, https etc.

 So for the moment I will give a dev install instruction. However, it is likely to become rather cumbersome at some point.

 # Installation for dev

1.) Clone this repo

> git clone https://github.com/fretchen/img-viewer

2.) Create a virtual enviromnment

> python3 -m venv venv

3.) Activate the virtualenv

> source venv/bin/activate

3.) Install the required packages:

> pip install -r requirements.txt

4.) Copy the 'config_example.ini' to 'config.ini' and adapt add experiments with names and folders where they are pointing.

> cp config_example.ini config.ini

5.) Initialize the database

> flask db upgrade

5.) Run the python app

> python app.py

6.) You can open the server on [localhost:8000](http://localhost:8000), but most likely it throwing some errors at the very first time as there are no entries.

7.) Refresh the database through [localhost:8000/refresh_db](http://localhost:8000/refresh_db)

You should see all the necessary images or open an issue here.

## gunicorn

We would like to get slightly safer than running the test server. So next step is
gunicorn

1.) Do a pip install of gunicorn

> pip install gunicorn

2.) Launch it

gunicorn -w 4 -b 127.0.0.1:8000 app:app
