import urllib.request
import time
import re
import html.parser
Url = 'https://ugra-news.ru/article/'

def change_date (date):
    odd = ['01', '03', '05', '07', '08', '10', '12']
    if date.startswith('01'):
        if date[2:4] in odd:
            #здесь меняется дата, потом надо вставить эту функцию во вложенный трай-эксепт

def obhod ():
    text = ''
    j = '29092017'
    for i in range(55928, 0, -1):
        pu = Url + j + str(i)
        try:
            page = urllib.request.urlopen(pu)
            print (pu)
            text += page.read().decode('ISO-8859-1')
        except:
            print ('PROBLEM ', pu)
            try:
                
            continue
    return text

def ochistka (text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    text = regScript.sub('', text)
    text = regComment.sub('', text)
    text = regTag.sub('', text)
    text = html.parser.HTMLParser().unescape(text)
    return text

def sozdanie (text):
    f = open('alban_corpus.txt', 'w', encoding = 'utf8')
    f.write(text)
    f.close

def main ():
    corpus = obhod()
    corpus = ochistka(corpus)
    sozdanie(corpus)

main ()
