from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

# main url
url = 'https://wikimon.net/Visual_List_of_Digimon'
web = requests.get(url)
soup = BeautifulSoup(web.content, 'html.parser')

# mysql connection
mydb = mysql.connector.connect(
        host = 'localhost' ,
        user = 'your username',
        passwd = 'your password',
        database = 'digimon'
    )

# web scrap data
name = []
piclink = []

for a in soup.find_all('div', id = 'mw-content-text'):
    for b in a.find_all('table', style = 'text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;'):
        for c in b.find_all('a'):
            if c.text == '':
                continue
            else:
                name.append(c.text)

for c in soup.find_all('div', id = 'mw-content-text'):
    for d in c.find_all('table', style = 'text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;'):
        for e in d.find_all('img'):
            piclink.append('https://wikimon.net' + e['src'])

listAll = []
n = 0

while n < len(name):
    listAll.append([name[n],piclink[n]])
    n += 1

# export to csv
with open('digimon.csv', 'w', newline = '', encoding = 'utf-8') as filedigimon:
    writer = csv.writer(filedigimon)
    writer.writerow(['name','picture link'])
    writer.writerows(listAll)

# export to mysql
x = mydb.cursor()

for i in range(len(listAll)):
    nama = listAll[i][0]
    gambar = listAll[i][1]
    x.execute(
    'insert into digimon(nama, gambar) values (%s, %s)',
    (nama, gambar)
    )

mydb.commit()
    