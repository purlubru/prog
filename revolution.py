from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import urllib.parse
import re
import html
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

url = 'http://www.intellicast.com/Local/Weather.aspx?unit=C&location=MKXX0001'
dict = 'http://www.dorev.ru/ru-index.html?s='
vowels = 'аяоёуюэеыиѣѵ'
consonants = 'цкнгшзхдлрпвфмтбсжчщ'

def mystem(s):
    f = open('s.txt', 'w', encoding='utf8')
    f.write(s)
    f.close()
    f = open('myst.txt', 'w', encoding='utf8')
    f.close()
    os.system(r".\mystem.exe " + "-nid " + 's.txt' + " " + 'myst.txt')

def find_lemma(w):
    f = open('myst.txt', 'r', encoding='utf8')
    file = f.read()
    f.close()
    try:
        lemma = re.search('{(.+?)=', file).group(1)
    except:
        lemma = w
        return lemma
    page = urllib.request.urlopen(dict + urllib.parse.quote(lemma.encode('windows-1251')))
    text = page.read().decode('windows-1251')
    r = ''
    t = True
    while t == True:
        try:
            r = re.search('color:#004488">(.+?)</span', text).group(1)
            text.seek(1, from_what=1)
        except:
            t = False
    if r != '':
        r = html.unescape(r)
    else:
        r = lemma
    return r

def changing(word, lemma):
    s = 0
    if word.startswith('бес'):
        s = 1
    if 'ѣ' in lemma:
        word = word.replace('е', 'ѣ')
    if 'ѵ' in lemma:
        word = word.replace('и', 'ѵ')
    if 'ѳ' in lemma:
        word = word.replace('ф', 'ѳ')
    if 'Ѳ' in lemma:
        word = word.replace('ф', 'Ѳ')
    word = list(word)
    for i in range(1, len(word)):
        if (word[i] in vowels) and (word[i-1] == 'и'):
            word[i-1] = 'i'
    if word[-1] in consonants:
        word.append('ъ')
    if s == 1:
        word[2] = 'з'
    return ''.join(word)

def clean_text (text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    text = regScript.sub('', text)
    text = regComment.sub('', text)
    text = regTag.sub('', text)
    text = html.unescape(text)
    return text

@app.route('/')
def index():
    page = urllib.request.urlopen(url)
    text = page.read().decode('utf8')
    n = re.search('title="Temperature">(.+?)</a>', text)
    t = html.unescape(n.group(1))
    return render_template('new_main.html', temperature=t)


@app.route('/res')
def res():
    print('hello')
    word = request.args['answer']
    word = word.lower()
    mystem(word)
    w = find_lemma(word)
    result = changing(word, w)
    return '<html><body><h1>{}</h1></body></html>'.format(result)

@app.route('/news')
def news():
    print('news is running')
    cin = 'http://www.cinemaholics.ru'
    page = urllib.request.urlopen(cin)
    t = page.read().decode('utf8')
    print('page opened')
    text = clean_text(t)
    print('text is ready')
    word = ''
    f = open('templates/kino.html', 'w', encoding='utf8')
    s = ''
    freq = {}
    for el in text:
        el = str(el)
        if el in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            word += el
        else:
            if word != '':
                print(word)
                mystem(word)
                l = find_lemma(word)
                if l in freq:
                    freq[l] += 1
                else:
                    freq[l] = 0
                new_word = changing(word.lower(), l)
                word = ''
                s += new_word + ' '
    print('all the words changed')
    i = 0
    s += '\n10 cамых частотных слов:\n'
    for k in sorted(freq.items()):
        if i == 10:
            break
        s += str(k) + '\n'
        print(s)
        i += 1
    print('frequencies are counted')
    f.write(s)
    f.close()
    return render_template('kino.html')

@app.route('/test')
def test():
    return render_template('yati.html')

if __name__ == '__main__':
    app.run(debug=True)