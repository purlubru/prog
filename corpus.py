import urllib.request
import time
import re
import html.parser
import os

Url = 'https://ugra-news.ru/article/'

class info:
    au = ''
    ti = ''
    da = ''
    url = ''

def change_date(date):
    date1 = list(date)
    odd = [1, 3, 5, 7, 8, 10, 12]
    eq = [4, 6, 9, 11]
    month = int(date[2:4])
    m = date[2:4]
    d = date[:2]
    if date.startswith('01'):
        if month-1 in odd:
            date1[0] = '3'
            date1[1] = '1'
        if month-1 in eq:
            date1[0] = '3'
            date1[1] = '0'
        if month-1 == 2:
            date1[0] = '2'
            if int(date[-4:])%4 == 0:
                date1[1] = '9'
            else:
                date1[1] = '8'
        if m.startswith('0'):
            if m.endswith('1'):
                date1[0] = '3'
                date1[1] = '1'
                date1[2] = '1'
                date1[3] = '2'
                date1[-1] = str(int(date[-1]) - 1)
            else:
                date1[3] = str(int(date[3]) - 1)
        if m.startswith('1'):
            if m.endswith('0'):
                date1[2] = '0'
                date1[3] = '9'
            else:
                date1[3] = str(int(date[3]) - 1)
    else:
        if d.startswith('0'):
            date1[1] = str(int(date[1]) - 1)
        else:
            if d.endswith('0'):
                print(date)
                date1[0] = str(int(date[0]) - 1)
                date1[1] = '9'
            else:
                date1[1] = str(int(date[1]) - 1)
    return ''.join(date1)

def clean_text (text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    text = regScript.sub('', text)
    text = regComment.sub('', text)
    text = regTag.sub('', text)
    text = html.unescape(text)
    return text

def read_text(text, pu):
    T = info()
    T.url = pu
    n = re.search('<h1>(.+?)</h1>', text)
    T.ti = html.unescape(n.group(1))
    n = re.search('<div class="field field-name-field-author field-type-taxonomy-term-reference field-label-above"><div class="field-label">Автор текста:&nbsp;</div><div class="field-items"><div class="field-item even"><a href=(.+?) typeof="skos:Concept" property="rdfs:label skos:prefLabel" datatype="">(.+?)</a></div></div></div>', text)
    if 'class="field-item odd"' in n.group(2):
        if n.group(2).startswith('Новости') or n.group(2).startswith('Местное') or n.group(2).startswith('Сургут') or n.group(2).startswith('Знамя') or n.group(2).startswith('Югорское'):
            m = re.search('(.+)>(.*)', n.group(2)) #Иногда есть два "автора": название газеты и само имя автора
            T.au = m.group(2)
        else:
            m = re.search('(.+?)</a>(.*)', n.group(2))
            T.au = m.group(1)
    else:
        T.au = n.group(2)
    n = re.search ('https://ugra-news.ru/article/(.+?)/', pu)
    date = n.group(1)
    T.da = date[:2] + '.' + date[2:4] + '.' + date[4:]
    r = re.compile('<div class="field field-name-body(.+?)>(.+?)</div></div></div>', re.DOTALL)
    res = r.search(text)
    news_text = res.group(2)
    news_text = clean_text(news_text)
    return news_text, T

def create_text(T, text, i):
    name = str(i) + '.txt'
    print ('name is ', name)
    s = '@au ' + T.au + '\n' + '@ti ' + clean_text(T.ti) + '\n' + '@da ' + T.da + '\n' + '@url ' + T.url + '\n'
    f = open(name, 'w', encoding = 'utf8')
    f.write(s)
    f.write(text)
    f.close()
    return name

def create_s(path, T):
    s = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tокружная\t%s\tugra-news.ru\t\t%s\tгазета\tРоссия\tЮгра\tru\n'
    s = s % (path, T.au, T.ti, T.da, T.url, T.da[-4:])
    return s

def changing(i, j):
    k = True
    while k:
        i = i - 1
        pu = Url + j + '/' + str(i)
        print ('new url ', pu)
        try:
            page = urllib.request.urlopen(pu)
            k = False
        except:
            continue
    return i

def mystem(path, name):
    os.chdir('C:\\Users\Полина\PycharmProjects\\newspapers')
    p = path.replace('plain', 'mystem-plain')
    pp = path.replace('plain', 'mystem-xml')
    if not os.path.exists(p):
        os.makedirs(p)
    if not os.path.exists(pp):
        os.makedirs(pp)
    f = open(p + '/' + name, 'w')
    xname = name.replace('.txt', '.xml')
    ff = open(pp + '/' + xname, 'w')
    text1 = path.replace('C:\\Users\Полина\PycharmProjects\\newspapers', '.') + '\\' + name
    text2 = p.replace('C:\\Users\Полина\PycharmProjects\\newspapers', '.') + '\\' + name
    text3 = pp.replace('C:\\Users\Полина\PycharmProjects\\newspapers', '.') + '\\' + xname
    os.system(r".\mystem.exe " + "-nid " + text1 + " " + text2) #запись в .txt
    os.system(r".\mystem.exe " + "-nid " + text1 + " " + text3) #запись в .xml
    f.close()
    ff.close()

def obhod():
    j = '02102017' #произвольная дата
    k = 0
    f = open('../metadata.csv', 'w', encoding = 'utf8')
    s = 'path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n'
    i = 56019 #произвольный номер статьи
    f.write(s)
    if not os.path.exists(j[-4:]):
        os.mkdir(j[-4:])
    os.chdir(j[-4:])
    if not os.path.exists(j[2:4]):
        os.mkdir(j[2:4])
    os.chdir(j[2:4])
    print ('i am at', os.getcwd())
    while i != 0:
        os.chdir('C:\\Users\Полина\PycharmProjects\\newspapers\\Ugra_news\plain')
        if not os.path.exists(j[-4:]):
            os.mkdir(j[-4:])
        os.chdir(j[-4:])
        if not os.path.exists(j[2:4]):
            os.mkdir(j[2:4])
        os.chdir(j[2:4])
        if k == 500:   #это счётчик файлов, чтобы не скачивать всю газету целиком, можно убрать
            break
        pu = Url + j + '/' + str(i)
        print ('opened ', pu)
        try:
            page = urllib.request.urlopen(pu)
            text = page.read().decode('utf8')
            text1, T1 = read_text(text, pu) #чтение ключевой информации и текста статьи
            name = create_text(T1, text1, i) #запись всего этого в файл
            dir = os.getcwd() + '\\' + name
            dir1 = os.getcwd()
            s = create_s(dir, T1) #создание строки .csv таблицы, соответствующей статье
            f.write(s)
            print('dir is ', dir)
            mystem(dir1, name)
            i -= 1 #следующая статья (я иду с самой новой к самой старой)
            k += 1
            time.sleep(2)
        except:
            j = change_date(j) #смена даты, да
            print ('new date: ', j)
            i = changing(i, j) #поиск номера статьи, который существует при заданной выше дате
            print ('new article: ', i)
    f.close()

def main():
    os.mkdir('Ugra_news')
    os.chdir('Ugra_news')
    os.mkdir('plain')
    os.chdir('plain')
    obhod()

main()