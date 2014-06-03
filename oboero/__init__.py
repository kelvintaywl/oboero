#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import random, json, urllib2
from views import index

app = Flask(__name__)
app.register_blueprint(index, url_prefix="")

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

