import urllib.request
import json
import datetime
import matplotlib.pyplot as plt

def to_dic(dic, s, n):
    if s not in dic:
        dic[s] = [n, 1]
    else:
        dic[s][0] += n
        dic[s][1] += 1
    return dic

def comment_job(id, dict, posts, cities, bdays):
    for item in dict['response']['items']:
        print('new comment')
        for i in range(len(posts)):
            l = posts[i].split(';')
            if l[0] == str(id):
                posts[i] = posts[i] + ';' + '\"' + item['text'].replace('\n', '') + '\"'
        a = item['text'].split()
        if not str(item['from_id']).startswith('-'):
            req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=bdate,city&v=5.73&access_token=d32a13edd32a13edd32a13edc3d3483f6cdd32ad32a13ed89ebf321ee7eb84b523e001d'.format(item['from_id']))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            data = json.loads(result)
            if 'city' in data['response'][0]:
                cities = to_dic(cities, data['response'][0]['city']['title'], len(a))
            if 'bdate' in data['response'][0]:
                date = data['response'][0]['bdate'].split('.')
                if len(date) == 3:      #бывает, что указывают дни рождения без года
                    bday = datetime.date(year=int(date[2]), month=int(date[1]), day=int(date[0]))
                    age = datetime.date.today() - bday
                    age = str(age).split()
                    age = round(int(age[0])/365)
                    bdays = to_dic(bdays, age, len(a))
    return posts, bdays, cities

def dic_to_xy(dic):
    dic_x = []
    dic_y = []
    for key in dic:
        dic_x.append(key)
        dic_y.append(dic[key][0]/dic[key][1])
    return dic_x, dic_y

offs = ['0', '100']
ids = []
posts = []
cities = {}
bdays = {}
for off in offs:
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-53845179&count=100&v=5.73&access_token=d32a13edd32a13edd32a13edc3d3483f6cdd32ad32a13ed89ebf321ee7eb84b523e001d&offset=' + off)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for item in data['response']['items']:
        ids.append(item['id'])
        s = str(item['id']) + ';' + '\"' + item['text'].replace('\n', ' ') + '\"'
        posts.append(s)
for id in ids:
    print('new post')
    data2 = []
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-53845179&count=100&post_id={}&v=5.73&access_token=d32a13edd32a13edd32a13edc3d3483f6cdd32ad32a13ed89ebf321ee7eb84b523e001d'.format(id))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    if data['response']['count'] > 100:
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-53845179&count=100&offset=100&post_id={}&v=5.73&access_token=d32a13edd32a13edd32a13edc3d3483f6cdd32ad32a13ed89ebf321ee7eb84b523e001d'.format(id))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data2 = json.loads(result)
    posts, bdays, cities = comment_job(id, data, posts, cities, bdays)
    if data2 != []:
        posts, bdays, cities = comment_job(id, data2, posts, cities, bdays)
print(posts)
print(cities)
print(bdays)
f = open('texts.csv', 'w', encoding='utf8')
f.write('id;post;comments')
for i in range(len(posts)):
    if not posts[i].endswith('\n'):
        posts[i] = posts[i] + '\n'
    f.write(posts[i])
f.close()
numbers = {}
p = 0
c = 0
for line in posts:
    l = line.split(';')
    if l[1] != '\"\"':
        p = len(l[1].split())
    if len(l) > 2:
        for i in range(2, len(l)):
            c += len(l[i].split())
        c = c / (len(l) - 2)
    numbers = to_dic(numbers, p, c)
numbers_x, numbers_y = dic_to_xy(numbers)
plt.bar(numbers_x, numbers_y)
plt.title('Соотношение длины поста со средней длиной комментариев')
plt.xlabel('Длина поста')
plt.ylabel('Средняя длина комментариев')
plt.show()
cities_x, cities_y = dic_to_xy(cities)
plt.bar(range(len(cities_x)), cities_y)
plt.title('Соотношение города пользователя и длины его комментария')
plt.xlabel('Город')
plt.ylabel('Средняя длина комментариев')
plt.xticks(range(len(cities_x)), cities_x, rotation=90)
plt.show()
bdays_x, bdays_y = dic_to_xy(bdays)
plt.bar(bdays_x, bdays_y)
plt.title('Соотношение возраста пользователя и длины его комментария')
plt.xlabel('Возраст')
plt.ylabel('Средняя длина комментариев')
plt.show()