from flask import Flask
from flask import request
from flask import render_template
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/res')
def res():
    if os.path.exists('anketa.csv'):
        f = open('anketa.csv', 'a', encoding='utf8')
    else:
        f = open('anketa.csv', 'w', encoding='utf8')
    for i in range(1, 15):
        s = 'answer' + str(i)
        a = request.args[s]
        f.write(a+'\t')
    f.write('\n')
    f.close()
    return '<html><body><h1>Спасибо!</h1></body></html>'

@app.route('/stats')
def stats():
    if os.path.exists('anketa.csv'):
        f = open('anketa.csv', 'r', encoding='utf8')
        text = f.read().split('\n')
        f.close()
        for i in range(len(text)):
            text[i] = text[i].split('\t')
        return render_template('answers.html', text=text)
    else:
        return '<html><body><h1>Извините, ответов на анкету ещё нет.</h1></body></html>'

@app.route('/json')
def js():
    if os.path.exists('anketa.csv'):
        f = open('anketa.csv', 'r', encoding='utf8')
        text = f.read().split('\n')
        f.close()
        for i in range(len(text)):
            text[i] = text[i].split('\t')
        json_str = json.dumps(text)
        return '<html><body>{}</body></html>'.format(json_str)
    else:
        return '<html><body><h1>Извините, ответов на анкету ещё нет.</h1></body></html>'

@app.route('/search')
def search():
    return render_template('poisk.html')

@app.route('/results')
def results():
    if os.path.exists('anketa.csv'):
        f = open('anketa.csv', 'r', encoding='utf8')
        text = f.read().split('\n')
        f.close()
        for i in range(len(text)):
            text[i] = text[i].split('\t')
        s = ''
        try:
            w = request.args['word']
            for i in text:
                for j in i:
                    if w in j:
                        s = s + j +'<br>'
        except:
            n = int(request.args['answer'])
            for i in range(len(text)-1):
                s = s + text[i][n-1] + '<br>'
        return '<html><body><h1>Результаты поиска:</h1><p>{}</p></body></html>'.format(s)
    else:
        return '<html><body><h1>Извините, ответов на анкету ещё нет.</h1></body></html>'

if __name__ == '__main__':
    app.run(debug=True)