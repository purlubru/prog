from flask import Flask
from flask import request
from flask import render_template
import gensim, logging
from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

app = Flask(__name__)

m = Mystem()
morph = MorphAnalyzer()

mo = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(mo, binary=True)
model.init_sims(replace=True)

def mystem_to_morphy(tag):
    for i, t in enumerate(tag):
        if t == 'род':
            tag[i] = 'рд'
        elif t == 'дат':
            tag[i] = 'дт'
        elif t == 'вин':
            tag[i] = 'вн'
        elif t == 'твор':
            tag[i] = 'тв'
        elif t == 'парт':
            tag[i] = 'рд2'
        elif t == 'местн':
            tag[i] = 'пр2'
        elif t == 'зват':
            tag[i] = 'зв'
        elif t == 'пов':
            tag[i] = 'повел'
        elif t == 'прев':
            tag[i] = 'превосх'
        elif t == '1-л':
            tag[i] = '1л'
        elif t == '2-л':
            tag[i] = '2л'
        elif t == '3-л':
            tag[i] = '3л'
        elif t == 'муж':
            tag[i] = 'мр'
        elif t == 'жен':
            tag[i] = 'жр'
        elif t == 'сред':
            tag[i] = 'ср'
    new_tag = []
    for t in tag:
        if (t != 'кр') and (t != 'притяж') and (t != 'несов') and (t != 'сов') and (t != 'непрош') and (t != 'полн') and (t != 'срав') and (t != 'инф') and (t != 'прич') and (t != 'деепр'):
            new_tag.append(t)
    return new_tag

def change_text(text):
    lemmas = m.lemmatize(text)
    w = m.analyze(text)
    for i in range(len(lemmas)):
        if re.search('[а-я|А-Я]', lemmas[i]):
            pos = w[i]['analysis'][0]['gr'].split(',')[0]
            word = lemmas[i] + '_' + pos
            if word in model:
                lemmas[i] = model.most_similar(positive=[word], topn=1)
    print(lemmas)
    for i, el in enumerate(w):
        word = el['text']
        if re.search('[а-я|А-Я]', word):
            tag2 = el['analysis'][0]['gr'].split('=')[1].split('|')[0].replace('(', '')
            if type(lemmas[i]) != str:
                lemmas[i] = lemmas[i][0][0].split('_')[0]
            if len(tag2) > 0:
                tag = morph.cyr2lat(','.join(mystem_to_morphy(tag2.split(','))))
                if len(tag) > 0:
                    tag = tag.split(',')
                    try:
                        lemmas[i] = morph.parse(lemmas[i])[0].inflect(set(tag)).word
                    except:
                        lemmas[i] = word
    return ''.join(lemmas)

@app.route('/')
def index():
    try:
        text = request.args['answer']
        new_text = change_text(text)
        new1 = text
        new2 = new_text
    except:
        new1 = ''
        new2 = ''
    return render_template('main.html', before=new1, after=new2)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mark')
def mark():
    f = open('marks.txt', 'r', encoding='utf8')
    file = f.read()
    f.close()
    marks = list(map(int, file.split(' ')))
    av = 0
    try:
        m = int(request.args['m'])
        marks[0] += m
        marks[1] += 1
        if marks[1] != 0:
            av = marks[0] / marks[1]
        f = open('marks.txt', 'w', encoding='utf8')
        s = str(marks[0]) + ' ' + str(marks[1])
        f.write(s)
        f.close()
    except:
        if marks[1] != 0:
            av = marks[0] / marks[1]
    return render_template('mark.html', average=av, value=(av*10))

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)