#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, make_response
from flask.blueprints import Blueprint
from .. import db
from oboero.models.verb import Verb, VerbQuestion
from oboero.services.verb_service import VerbService
blueprint = Blueprint('verb', __name__)


@blueprint.route('/')
def list():
    verbs = db.session.query(Verb).all()

    return render_template('verb/index.html', verb="VeRb", verbs=verbs)


@blueprint.route('/add')
def add():
    return render_template('verb/add.html')


@blueprint.route('/conjugate')
def conjugate():
    verb_service = VerbService()
    teinei = request.args.get('teinei')
    group = request.args.get('group', type=int)
    teinei, casual, te, potential, conditional, passive, causative = \
        verb_service.get_forms(teinei, group)

    verb = {'teinei': teinei, 'casual': casual, 'te': te,
            'potential': potential, 'conditional': conditional,
            'passive': passive, 'causative': causative}

    response = make_response(verb, 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@blueprint.route('/new', methods=['POST'])
def new():
    teinei, q_teinei = request.form.get('teinei'), request.form.get('q_teinei')
    casual, q_casual = request.form.get('casual'), request.form.get('q_casual')
    te, q_te = request.form.get('te'), request.form.get('q_te')
    potential, q_potential = request.form.get('potential'), request.form.get('q_potential')
    conditional, q_conditional = request.form.get('conditional'), request.form.get('q_conditional')
    passive, q_passive = request.form.get('passive'), request.form.get('q_passive')
    causative, q_causative = request.form.get('causative'), request.form.get('q_causative')

    verb = Verb(teinei=teinei, casual=casual, te=te, potential=potential,
                conditional=conditional, passive=passive, causative=causative)

    question = VerbQuestion(teinei=q_teinei, casual=q_casual, te=q_te, potential=q_potential,
                            conditional=q_conditional, passive=q_passive, causative=q_causative)

    verb.questions.append(question)
    db.session.add(verb)
    db.session.commit()
    return redirect(url_for('verb.list'))



