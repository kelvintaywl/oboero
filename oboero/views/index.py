#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, current_app, make_response
from flask.blueprints import Blueprint
from flask.ext.login import login_user, logout_user, current_user
import random
import json

from .. import db
from oboero.models.user import User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def game():
    state = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
                    for x in xrange(32))

    session['state'] = state
    client_id = current_app.config['CLIENT_ID']
    return render_template('game.html', verbs=[], total=0,
                           client_id=client_id, state=state)


@blueprint.route('/about')
def about():
    return render_template('about.html')


@blueprint.route('/profile')
def profile():
    assert current_user is not None
    return render_template('profile.html')

@blueprint.route('/save_profile', methods=['POST'])
def save_profile():
    _pic_url = request.form.get('pic_url')
    user_email = request.form.get('user_email', current_user.email)
    user = db.session.query(User).get(user_email)
    if not user:
        user = User(email=user_email, username=user_email.split('@')[0], pic_url=_pic_url.split('?sz')[0] + "?sz=70")
        db.session.add(user)
        db.session.commit()
    elif not user.pic_url:
        user.pic_url = pic_url=_pic_url.split('?sz')[0] + "?sz=70"
        db.session.commit()
    response = make_response(json.dumps('PICTURE SAVED'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@blueprint.route('/change_name', methods=['POST'])
def change_name():
    user = db.session.query(User).get(current_user.email)
    new_username = request.form.get('new_name') or "Incognito"
    new_username = new_username.strip()
    user.username = new_username
    db.session.commit()
    response = make_response(json.dumps('NAME SAVED'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@blueprint.route('/connect', methods=['POST'])
def login():
    # currently supported login options: Google Plus

    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # del session['state']
    code = request.data

    try:
        g_scopes = ['https://www.googleapis.com/auth/plus.login',
                    'https://www.googleapis.com/auth/plus.profile.emails.read']
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope=' '.join(g_scopes))
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session['credentials'] = credentials
    session['gplus_id'] = gplus_id

    user_email = credentials.id_token['email']
    user = db.session.query(User).get(user_email)
    if not user:
        # create user account in our db
        user = User(email=user_email, username=user_email.split('@')[0])
        db.session.add(user)
        db.session.commit()
    session['user'] = user
    login_user(user)

    response = make_response(json.dumps('Logged In!'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@blueprint.route('/logout', methods=['POST'])
def logout():
    credentials = session.get('credentials')
    if credentials:
        session.pop('credentials')
    if session.get('gplus_id'):
        session.pop('gplus_id')
    logout_user()
    print(current_user.is_authenticated())
    response = make_response(json.dumps('SIGNED OUT'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


