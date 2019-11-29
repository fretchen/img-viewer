from app import app, db
from app.models import User
from datetime import datetime
import os

import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
if len(sys.argv) == 3:
    print('Let us proceed');
    username = sys.argv[1];
    password = sys.argv[2];
    print('Suggested username = {}'.format(username));
    print('Suggested password = {}'.format(password));
    u = User(username=username);
    u.set_password(password);
    db.session.add(u);
    db.session.commit();
else:
    print('Wrong number of inputs');
