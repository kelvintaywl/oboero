import os

DEBUG = True
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
