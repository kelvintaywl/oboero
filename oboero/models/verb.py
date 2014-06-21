#!/usr/bin/python
# -*- coding: utf-8 -*-
from oboero import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

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

    questions = relationship("VerbQuestion", backref="verb")

class VerbQuestion(db.Model):
    __tablename__ = "verb_question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teinei = db.Column(db.String(25), nullable=True)  # kobini ni (ikimasu).
    casual = db.Column(db.String(25), nullable=True)  # masugu (iku) to, kobini ga miemasu.
    te = db.Column(db.String(25), nullable=True)  # itsu (itte) tara ii desuka?
    potential = db.Column(db.String(25), nullable=True)  # nanji kara (ikeru)?
    conditional = db.Column(db.String(25), nullable=True)  # doko ni (ikeba) ii desuka?
    passive = db.Column(db.String(25), nullable=True)  # robot ga (ikare).
    causative = db.Column(db.String(25), nullable=True)  # kare wa watashi ni jimu wo (ikaseru)
    verb_id = db.Column(db.Integer, ForeignKey('verb.id'))
