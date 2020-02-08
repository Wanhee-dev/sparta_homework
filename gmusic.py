import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbwanhee


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200204',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
rank = 0

for song in songs:
    title = song.select_one('td.info > a.title.ellipsis')
    if title is not None:
        rank += 1
        title = title.text
        artist = song.select_one('td.info > a.artist.ellipsis').text

    doc = {
        'title' : title,
        'rank' : rank,
        'artist' : artist
    }

    db.songs.insert_one({'title': title, 'rank': rank, 'artist': artist})