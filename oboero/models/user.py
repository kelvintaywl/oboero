#!/usr/bin/python
# -*- coding: utf-8 -*-

class User(object):
    # required methods for Flask-login
    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.email