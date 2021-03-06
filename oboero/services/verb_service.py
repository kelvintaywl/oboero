#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from sqlalchemy import func
from oboero.models.verb import Verb
from oboero import db

formTable = {
                    # a - i - u - e - o
            u"い": [u'わ', u'い', u'う', u'え', u'お'],
            u"ち": [u'た', u'ち', u'つ', u'て', u'と'],
            u"り": [u'ら', u'り', u'る', u'れ', u'ろ'],
            u"き": [u'か', u'き', u'く', u'け', u'こ'],
            u"ぎ": [u'が', u'ぎ', u'ぐ', u'げ', u'ご'],
            u"み": [u'ま', u'み', u'む', u'め', u'も'],
            u"び": [u'ば', u'び', u'ぶ', u'べ', u'ぼ'],
            u"し": [u'さ', u'し', u'す', u'せ', u'そ']
}

class VerbService(object):
    def __init__(self):
        pass

    def get_forms(self, teinei, group):
        verb = {'jap': teinei, 'group': group}
        casual = self.to_plain(verb)
        te = self.to_te(verb)
        potential = self.to_potential(verb)
        conditional = self.to_conditional(verb)
        passive = self.to_passive(verb)
        causative = self.to_causative(verb)

        return (teinei, casual, te, potential, conditional, passive, causative)



    def to_plain(self, verb):
        #print verb
        if verb['group'] == 1:
            lastChar = verb['jap'][-1:]
            newChar = formTable[lastChar][2] # u letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'る')
        else:
            ki = u'来'
            shi = u'し'
            if verb['jap'].find(ki) > -1:
                return (verb['jap'][:-1] + u'くる')
            else:
                return (verb['jap'][:-1] + u'する')
    
    def to_te(self, verb):
        front = self._to_t(verb)
        return (front + u'で') if verb['jap'][-1:] in [u'ぎ', u'び', u'み'] else (front + u'て')

    def _to_t(self, verb):
        if verb['group'] == 1:
            lastChar = verb['jap'][-1:]
            newChar = lastChar
            if lastChar in [u'い', u'ち', u'り']:
                newChar = u'っ'
            elif lastChar in [u'き', u'ぎ']:
                if verb['jap'] == u'行き':
                    newChar = u'っ'
                else:
                    newChar = u'い'
            elif lastChar in [u'び', u'み']:
                newChar = u'ん'
            else:
                newChar = u'し'
            return (verb['jap'][:-1] + newChar)
        else:
            return verb['jap']


    def to_nai(self, verb):
        if verb['group'] == 1:
            newChar = formTable[verb['jap'][-1:]][0] + u'ない' # a letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'ない')
        else:
            if verb['jap'][-1:] == u'来':
                return (verb['jap'][:-1] + u"こない")
            else: #group3 shimasu verb
                return (verb['jap'] + u'ない')

    def to_prohibitive(self, verb): #dependency: toPlain()
        return (self.to_plain(verb) + u'な')

    def to_imperative(self, verb):
        if verb['group'] == 1:
            newChar = formTable[verb['jap'][-1:]][3] # e letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'ろ')
        else:
            if verb['jap'][-1:] == u'来':
                return (verb['jap'][:-1] + u"こい")
            else:
                return (verb['jap'] + u"ろ")

    def to_volitional(self, verb):
        if verb['group'] == 1:
            newChar = formTable[verb['jap'][-1:]][3] + u'う' # o letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'よう')
        else:
            if verb['jap'][-1:] == u'来':
                return (verb['jap'][:-1] + u"こよう")
            else: #group3 shimasu verb
                return (verb['jap'] + u'よう')

    def to_potential(self, verb):
        if verb['group'] == 1:
            newChar = formTable[verb['jap'][-1:]][3] + u'る' # e letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'られる')
        else:
            if verb['jap'][-1:] == u'来':
                return (verb['jap'][:-1] + u"来られる")
            else: #group3 shimasu verb
                return (verb['jap'] + u'できる')

    def to_conditional(self, verb):
        if verb['group'] == 1:
            lastChar = verb['jap'][-1:]
            newChar = formTable[lastChar][3] + u'ば' # e letter
            return (verb['jap'][:-1] + newChar)
        elif verb['group'] == 2:
            return (verb['jap'] + u'れば')
        else:
            ki = u'来'
            shi = u'し'
            if verb['jap'].find(ki) > -1:
                return (verb['jap'][:-1] + u'くれば')
            else:
                return (verb['jap'][:-1] + u'すれば')

    def to_causative(self, verb):
        if verb['group'] == 1:
            return (self.to_nai(verb)[:-2] + u'せる')
        elif verb['group'] == 2:
            return (self.to_plain(verb)[:-1] + u'させる')
        else:
            if u'来' in verb:
                return u'こさせる'
            else:
                return u'させる'

    def to_passive(self, verb):
        if verb['group'] == 1:
            return self.to_nai(verb)[:-2] + u'れる'
        elif verb['group'] == 2:
            return self.to_plain(verb)[:-1] + u'られる'
        else:
            if u'来' in verb:
                return u'来られる'
            else:
                return u'される'

    def add_word(self, teinei, group):
        teinei, casual, te, potential, conditional, passive, causative = \
            self.get_forms(teinei, group)

        verb = Verb(teinei=teinei, casual=casual, te=te, potential=potential,
                    conditional=conditional, passive=passive, causative=causative)
        db.session.add(verb)

    def get_random(self):
        min_id = db.session.query(func.min(Verb.id)).one()[0]
        max_id = db.session.query(func.max(Verb.id)).one()[0]

        rand_id = random.randint(min_id, max_id)
        print("random; %d" % rand_id)
        verb = db.session.query(Verb).get(rand_id)

        print(dir(verb))

        form_type = random.choice(dir(verb))
        return verb, form_type