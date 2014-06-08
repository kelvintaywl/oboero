import os

DEBUG = True
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
CLIENT_ID = "932922823080-jstc80ffvoi6jklll2tej55pcidvj06q.apps.googleusercontent.com"
CLIENT_SECRET = "eMfsXiaWzgw-NvlYN-xZBmfW"
REDIRECT_URIS = ["https://localhost:5000/oauth2callback", "http://oboero.herokuapp.com/oauth2callback"]
