#!/usr/bin/python
# -*- coding: utf-8 -*-
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
        casual = toPlain(verb)
        te = toTe(verb)
        potential = toPotential(verb)
        conditional = toConditional(verb)
        passive = toPassive(verb)
        causative = toCausative(verb)

        return (teinei, casual, te, potential, conditional, passive, causative)



    def toPlain(self, verb):
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
    
    def toTe(self, verb):
        front = toT(verb)
        return (front + u'で') if verb['jap'][-1:] in [u'ぎ', u'び', u'み'] else (front + u'て')

    def toT(self, verb):
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


    def toNai(self, verb):
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

    def toProhibitive(self, verb): #dependency: toPlain()
        return (toPlain(verb) + u'な')

    def toImperative(self, verb):
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

    def toVolitional(self, verb):
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

    def toPotential(self, verb):
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

    def toConditional(self, verb):
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

    def toCausative(self, verb):
        if verb['group'] == 1:
            return (toNai(verb)[:-2] + u'せる')
        elif verb['group'] == 2:
            return (toPlain(verb)[:-1] + u'させる')
        else:
            if u'来' in verb:
                return u'こさせる'
            else:
                return u'させる'

    def toPassive(self, verb):
        if verb['group'] == 1:
            return toNai(verb)[:-2] + u'れる'
        elif verb['group'] == 2:
            return toPlain(verb)[:-1] + u'られる'
        else:
            if u'来' in verb:
                return u'来られる'
            else:
                return u'される'

