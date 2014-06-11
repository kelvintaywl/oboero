#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, jsonify, request, redirect, url_for, g, session, current_app, make_response
from flask.blueprints import Blueprint
from flask.ext.login import login_user, logout_user, current_user
import random, json, urllib2, urllib

from .. import db
from oboero.models.user import User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def game():

    # redirect user to profile page if already logged in
    #if current_user is not None and current_user.is_authenticated():
        #return redirect(url_for('index.profile'))

    state = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
                         for x in xrange(32))
    session['state'] = state
    client_id = current_app.config['CLIENT_ID']
    return render_template('game.html', verbs=[], total=0, client_id=client_id, state=state)

@blueprint.route('/about')
def about():
    return render_template('about.html')

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
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.profile.emails.read')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade authorization code'), 401)
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

    print(current_user is None)
    response = make_response(json.dumps('SIGNED OUT'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@blueprint.route('/profile')
def profile():
    assert current_user is not None
    return render_template('profile.html')

