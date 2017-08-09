from bs4 import BeautifulSoup as BS
import urllib3
import io

url = 'http://imgur.com/a/TuT7t'
http = urllib3.PoolManager()

html = http.urlopen('GET',url)

soup = BS(html.data, "html.parser")

data = soup.find_all('div', attrs={'class':'post-image'})

links = []
for a in data:
    for b in a:
        if b.name == 'a':
            links.append('https://' + b['href'][2:])

print(links)