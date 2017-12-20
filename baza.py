import sqlite3
import matplotlib.pyplot as plt

pos = ['ADJ', 'ADV', 'AUX', 'COMP', 'CONJ', 'CONN', 'DEM', 'N', 'NUM', 'P', 'PART', 'PRON', 'PRV', 'PTCP', 'V', 'Q', 'ENCL']
cases = ['LOC', 'NOM', 'GEN', 'DAT', 'ACC', 'DAT-LOC', 'INSTR', 'VOC', 'ABL']
verbs = ['2SG', '1PL', '1SG', '3PL', '3SG']
verbs2 = ['INF', 'IMP', 'PRS', 'MED']

source = sqlite3.connect('hittite.db')
s = source.cursor()
result = sqlite3.connect('new_data.db')
r = result.cursor()
r.execute('CREATE TABLE words (id INTEGER PRIMARY KEY, Lemma TEXT, Wordform TEXT, Glosses TEXT)')
r.execute('CREATE TABLE glosses (glossid INTEGER PRIMARY KEY, обозначение TEXT, расшифровка TEXT)')
r.execute('CREATE TABLE wordsglosses (word_id, gloss_id)')
for row in s.execute('SELECT * FROM wordforms'):
    a = str(row)[1:-1]
    a = a.replace(' ', '')
    a = a.replace('\'', '')
    a = a.split(',')
    r.execute('INSERT INTO words (Lemma, Wordform, Glosses) VALUES (?, ?, ?)', (a[0], a[1], a[2]))
f = open('Glossing_rules.txt', 'r', encoding='utf8')
file = f.read().split('\n')
f.close()
for line in file:
    l = line.split(' ')
    r.execute('INSERT INTO glosses (обозначение, расшифровка) VALUES (?, ?)', (l[0], l[2]))
i = 1
for row in s.execute('SELECT Glosses FROM wordforms'):
    a = str(row)[1:-1].replace('\'', '').replace(',', '').split('.')
    n = 0
    for g in a:
        if str(g).isupper():
            a.append(r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (g,)).fetchone())
            if a[-1] == None:
                r.execute('INSERT INTO glosses (обозначение) VALUES (?)', (g,))
                a[-1] = r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (g,)).fetchone()
            n += 1
    for k in range(1, n + 1):
        y = str(a[-1 * k]).replace('(', '').replace(')', '').replace(',', '')
        r.execute('INSERT INTO wordsglosses (word_id, gloss_id) VALUES (?, ?)', (str(i), str(y)))
    i += 1
source.close()
plt.figure(1)
plt.subplot(221)
X = range(len(pos))
Y = []
for p in pos:
    n = int(str(r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (p,)).fetchone()).replace('(', '').replace(')', '').replace(',', ''))
    c = r.execute('SELECT word_id FROM wordsglosses WHERE gloss_id=?', (str(n),)).fetchall()
    if c:
        Y.append(len(c))
    else:
        Y.append(0)
plt.bar(X, Y)
plt.xticks(X, pos)
plt.title('Части речи')
plt.subplot(222)
X = range(len(cases))
Y = []
for c in cases:
    n = int(str(r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (c,)).fetchone()).replace('(', '').replace(')', '').replace(',', ''))
    count = r.execute('SELECT word_id FROM wordsglosses WHERE gloss_id=?', (str(n),)).fetchall()
    Y.append(len(count))
plt.bar(X, Y)
plt.xticks(X, cases)
plt.title('Падежи')
plt.subplot(223)
X = range(len(verbs))
Y = []
for el in verbs:
    n = int(str(r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (el,)).fetchone()).replace('(', '').replace(')', '').replace(',', ''))
    count = r.execute('SELECT word_id FROM wordsglosses WHERE gloss_id=?', (str(n),)).fetchall()
    Y.append(len(count))
plt.bar(X, Y)
plt.xticks(X, verbs)
plt.title('Лично-числовые показатели')
plt.subplot(224)
X = range(len(verbs2))
Y = []
for el in verbs2:
    n = int(str(r.execute('SELECT glossid FROM glosses WHERE обозначение=?', (el,)).fetchone()).replace('(', '').replace(')', '').replace(',', ''))
    count = r.execute('SELECT word_id FROM wordsglosses WHERE gloss_id=?', (str(n),)).fetchall()
    Y.append(len(count))
plt.bar(X, Y)
plt.xticks(X, verbs2)
plt.title('Другие глагольные показатели')
plt.show()
result.commit()
result.close()