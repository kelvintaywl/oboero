#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify, url_for, g
import httplib2

from simplekv.memory import DictStore
from flask.ext.kvsession import KVSessionExtension
from apiclient.discovery import build

import urllib
import random
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
db = SQLAlchemy()
lm = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
                         for x in xrange(32))

    store = DictStore()
    KVSessionExtension(store, app)
    app.SERVICE = build('plus', 'v1')

    db.init_app(app)
    lm.init_app(app)
    from views import index, verb
    
    # register blueprints
    app.register_blueprint(index.blueprint, ur_prefix="")
    app.register_blueprint(verb.blueprint, url_prefix="/verb")


    # set login logic
    public_endpoints = ['index.game', 'index.login',
                        'index.about', 'verb.list', 'static']

    def login_valid():
    	return current_user is not None and current_user.is_authenticated()

    def login_redirect():
    	return redirect(url_for('index.game'))

    @app.before_request
    def _before_request():
    	if request.endpoint not in public_endpoints and not login_valid():
            return login_redirect()

        return

    @lm.user_loader
    def load_user(email):
        from oboero.models.user import User
        from . import db
        return db.session.query(User).get(email)

    return app

