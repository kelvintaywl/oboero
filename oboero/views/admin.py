#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from flask.blueprints import Blueprint
from .. import db
from oboero.models.verb import Verb
from oboero.services.verb_service import VerbService
blueprint = Blueprint('admin', __name__)


@blueprint.route('/verb')
def verb_list():
    verbs = db.session.query(Verb).all()

    return render_template('verb/index.html', verb="VeRb", verbs=verbs)


@blueprint.route('/verb/add')
def verb_add():
    return render_template('verb/add.html')


@blueprint.route('/verb/new', methods=['POST'])
def verb_new():
    verb_service = VerbService()
    teinei = request.form.get('teinei')
    group = request.form.get('group', type=int)
    teinei, casual, te, potential, conditional, passive, causative = verb_service.get_forms(teinei, group)
    print(conditional)

    verb = Verb(teinei=teinei, casual=casual, te=te, potential=potential,
                conditional=conditional, passive=passive, causative=causative)
    db.session.add(verb)
    db.session.commit()
    return redirect(url_for('admin.verb_list'))



