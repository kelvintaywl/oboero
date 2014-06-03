#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import random, json, urllib2

app = Flask(__name__)


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




def toPlain(verb):
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
def toTe(verb):
    front = toT(verb)
    return (front + u'で') if verb['jap'][-1:] in [u'ぎ', u'び', u'み'] else (front + u'て')

def toT(verb):
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


def toNai(verb):
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

def toProhibitive(verb): #dependency: toPlain()
    return (toPlain(verb) + u'な')

def toImperative(verb):
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

def toVolitional(verb):
    if verb['group'] == 1:
        newChar = formTable[verb['jap'][-1:]][4] + u'う' # o letter
        return (verb['jap'][:-1] + newChar)
    elif verb['group'] == 2:
        return (verb['jap'] + u'よう')
    else:
        if verb['jap'][-1:] == u'来':
            return (verb['jap'][:-1] + u"こよう")
        else: #group3 shimasu verb
            return (verb['jap'] + u'よう')

def toConditional(verb):
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

def toCausative(verb):
    if verb['group'] == 1:
        return (toNai(verb)[:-2] + u'せる')
    elif verb['group'] == 2:
        return (toPlain(verb)[:-1] + u'させる')
    else:
        if u'来' in verb:
            return u'こさせる'
        else:
            return u'させる'

def toPassive(verb):
    if verb['group'] == 1:
        return toNai(verb)[:-2] + u'れる'
    elif verb['group'] == 2:
        return toPlain(verb)[:-1] + u'られる'
    else:
        if u'来' in verb:
            return u'来られる'
        else:
            return u'される'

def getWord(verb, rand):
    answer = '';
    if rand == 8:
        return toCausative(verb)
    elif rand == 7:
        return toPassive(verb)
    elif rand == 6:
        return toConditional(verb)
    elif rand == 5:
        return toVolitional(verb)
    elif rand == 4:
        return toImperative(verb)
    elif rand == 3:
        return toProhibitive(verb)
    elif rand == 2:
        return toNai(verb)
    elif rand == 1:
        return toTe(verb)
    else:
        return toPlain(verb)

def getForm(num):
    verbForm = '';
    if num == 8:
        return 'causative(saseru)'
    if num == 7:
        return 'passive(sareru)'
    elif num == 6:
        return 'conditional(sureba)'
    elif num == 5:
        return 'volitional(shiyo-)'
    elif num == 4:
        return 'imperative(shiro)'
    elif num == 3:
        return 'prohibitive(suruna)'
    elif num == 2:
        return 'negative(shinai)'
    elif num == 1:
        return 'te(shite)'
    else:
        return 'plain(suru)'

@app.route('/')
def game():
    verbs = _get_words_from_spreadsheets()
    for verb in verbs:
        ran = random.randint(0,8)
        verb['groupType'] = getForm(ran)
        verb['answer'] = getWord(verb, ran)
    return render_template('game.html', verbs=verbs, total=len(verbs))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return render_template('search.html')

#web service
@app.route('/api/verbs')
def get_verbs():
    verbs = _get_words_from_spreadsheets()
    return jsonify({'verbs': verbs})


@app.route('/api/verbs/random')
def get_random_verb():
    verbs = _get_words_from_spreadsheets()
    verb = verbs[random.randint(0,len(verbs)-1)]
    return jsonify({'verb': verb})

def _get_words_from_spreadsheets():
    #Google Spreadsheet Entrypoint URL: https://docs.google.com/spreadsheet/ccc?key=0As-5mxk3uTUOdDJIbDJfNng3aGJiQW1Ha21OUUhqaUE#gid=0
    spreadsheet_urls = ["https://spreadsheets.google.com/feeds/list/0As-5mxk3uTUOdDJIbDJfNng3aGJiQW1Ha21OUUhqaUE/1/public/values?alt=json", "https://spreadsheets.google.com/feeds/list/0As-5mxk3uTUOdDJIbDJfNng3aGJiQW1Ha21OUUhqaUE/3/public/values?alt=json"]
    #json.feed.entry is array = js
    verbs = []
    for url in spreadsheet_urls:
        content = urllib2.urlopen(url).read()
        data = json.loads(content)
        items = data['feed']['entry']
        for item in items:
            japVerb = item['gsx$wordmasu']['$t']
            verb = {"jap":japVerb, "group":int(item['gsx$group']['$t'])}
            verb.update({'plain': toPlain(verb),
                         'nai': toNai(verb),
                         'te': toTe(verb),
                         'conditional': toConditional(verb),
                         'prohibitive': toProhibitive(verb),
                         'imperative': toImperative(verb),
                         'volitional': toVolitional(verb),
                         'passive': toPassive(verb),
                         'causative': toCausative(verb)})
            verbs.append(verb)

    return verbs

if __name__ == '__main__':
    app.run()

