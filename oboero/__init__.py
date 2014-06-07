#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify, url_for, g
import urllib
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user

db = SQLAlchemy()
lm = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = '42'
    db.init_app(app)
    lm.init_app(app)
    from views import index, verb
    
    # register blueprints
    app.register_blueprint(index.blueprint, ur_prefix="")
    app.register_blueprint(verb.blueprint, url_prefix="/verb")


    # set login logic
    public_endpoints = ['index.game', 'index.login', 'index.about', 'verb.list', 'static']

    def login_valid():
    	return current_user is not None and current_user.is_authenticated()

    def login_redirect():
    	return redirect(url_for('index.login', next=urllib.quote_plus(request.url)))

    @app.before_request
    def _before_request():
    	if request.endpoint not in public_endpoints and not login_valid():
            return login_redirect()

        return

    return app

#dictionary of verbs

#verbs = [
                    #testing
#            {'jap': u'遊び', 'rom': 'asobi', 'eng': 'play', 'group': 1},
#            {'jap': u'行き', 'rom': 'iki', 'eng': 'go', 'group': 1},
#            {'jap': u'飲み', 'rom': 'nomi', 'eng': 'drink', 'group': 1},
#            {'jap': u'待ち', 'rom': 'machi', 'eng': 'wait', 'group': 1},
#            {'jap': u'話し', 'rom': 'hanashi', 'eng': 'talk', 'group': 1},
#            {'jap': u'食べ', 'rom': 'tabe', 'eng': 'eat', 'group': 2},
#            {'jap': u'起き', 'rom': 'oki', 'eng': 'wake up', 'group': 2},
#            {'jap': u'し', 'rom': 'shi', 'eng': 'do', 'group': 3},
#            {'jap': u'来', 'rom': 'ki', 'eng': 'come', 'group': 3},
#            {'jap': u'持って来', 'rom': 'motteki', 'eng': 'bring', 'group': 3},
#            {'jap': u'勉強し', 'rom': 'benkyoshi', 'eng': 'study', 'group': 3}
#]

