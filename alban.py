import urllib.request
import time
import re
import html.parser
Url = 'http://www.forumishqiptar.com/threads/'

def obhod ():
    text = ''
    for i in range(50, 100):
        pu = Url + str(i)
        #j = 1
        try:
            page = urllib.request.urlopen(pu)
            print ('hello')
            #while j:
               # pu = pu + '/page' + str(j)
               # if '#post' in pu.geturl():
                #    print ('page don\'t exist')
                #    break
            text += page.read().decode('ISO-8859-1')
            #    j += 1
        except:
            print ('PROBLEM ', pu)
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

#ВОПРОСЫ
#Программа почему-то считает все страницы существующими (даже те, на которых тредов нет), что с этим делать?
#Блок про просмотр всех страниц треда пока не работает, поэтому не смотрите туда особенно

