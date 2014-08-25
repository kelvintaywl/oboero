#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import jsonify
from flask.blueprints import Blueprint
from oboero.services.verb_service import VerbService
blueprint = Blueprint('verb', __name__)


@blueprint.route('/random')
def random():
    verb, form_type = VerbService().get_random()
    conjugated_form = getattr(verb, form_type)
    return jsonify(formal=verb.teinei, type=form_type, conjugated=conjugated_form)
