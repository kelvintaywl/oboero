#!/usr/bin/python
# -*- coding: utf-8 -*-
from oboero import db

class Verb(db.Model):
    __tablename__ = "verb"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teinei = db.Column(db.String(25), nullable=False)  # ikimasu
    casual = db.Column(db.String(25), nullable=False)  # iku
    te = db.Column(db.String(25), nullable=False)  # itte
    potential = db.Column(db.String(25), nullable=False)  # ikeru
    conditional = db.Column(db.String(25), nullable=False)  # ikeba
    passive = db.Column(db.String(25), nullable=False)  # ikareru
    causative = db.Column(db.String(25), nullable=False)  # ikaseru
