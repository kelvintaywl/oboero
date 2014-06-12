#!/usr/bin/python
# -*- coding: utf-8 -*-
from oboero import db
class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pic_url = db.Column(db.String(64))

    def __init__(self, email, username):
        self.email = email
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % self.name
