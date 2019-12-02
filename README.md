# Img-viewer

 Look into the shots we took with labscriptsuite. It is a great way to keep the
 larger public like the PI in the loop on what is going on in the lab. The software
 stack is really just [flask](https://palletsprojects.com/p/flask/) with some gimmicks around it.

 While this program can be installed on your personal PC
 for dev purposes it is not super useful there as we typically have easily thousands and thousands of images to
 crawl through. So this project is typically really designed to run on a public server.
 This also comes with quite a bit of tools around the core functionality that we
 need to implement to secure it like servers, login, https etc. Right now we are running it under:
 
 https://imgviewer.synqs.de

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

8.) To see the images you have to log in, which means that you need to create a first user.

> python create_user.py USERNAME PASSWORD

You should see all the necessary images or open an issue here.



# Deployment

while it is ok to use the img-viewer on a localhost it is actually really thought for servers. So here, we will discuss the necessay step to make it work.

## Set up

Start a ubuntu machine, then we have to set up supervisorctl, nginx. We are massively following the tutorial by
[Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux).

### supervisorctl
It allows us to automatically run on the system. We can give it the config file, which lives in
_/etc/supervisor/conf.d/imgviewer.conf_:

```
[program:imgviewer]
command=/home/ubuntu/venv/bin/gunicorn -b localhost:8000 -w 4 --log-level=warning app:app
directory=/home/ubuntu/git/img-viewer
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

Then you can start it through
> sudo supervisorctl start

For public usage you also would like to assign a permanent address and certificate.

## Updates

Given that we are running nginx continously we have to run in the simplest case:

> git pull
> pip install -r requirements.txt
> sudo supervisorctl reload

To stop nginx you have to run:

> sudo service nginx stop

## Debug

Stop superviorctl and nginx:

gunicorn -w 4 -b 127.0.0.1:8000 app:app
