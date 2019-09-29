import requests
import plotly.graph_objects as go
from bs4 import BeautifulSoup as bs

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

base_url = 'https://www.kinopoisk.ru/top/'

def py_scraper(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    years = []

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('td', attrs={'style': 'height: 27px; vertical-align: middle; padding: 6px 30px 6px 0'})

        for div in divs:
            film = div.find('a', attrs={'class': 'all'}).text
            year = ''

            for i in range(len(film)):
                if film[i] == '(':
                    year += film[i+1] + film[i+2] + film[i+3] + film[i+4]

            years.append(year)

    else:
        print('ERROR')

    return years

def drawing(years):
    values = []

    for i in range(10):
        values.append(0)

    for i in range(len(years)):
        values[int(years[i][2])] += 1

    labels = ['2000s (' + str(values[0]) + ' films)',
              '2010s (' + str(values[1]) + ' films)',
              '1920s (' + str(values[2]) + ' films)',
              '1930s (' + str(values[3]) + ' films)',
              '1940s (' + str(values[4]) + ' films)',
              '1950s (' + str(values[5]) + ' films)',
              '1960s (' + str(values[6]) + ' films)',
              '1970s (' + str(values[7]) + ' films)',
              '1980s (' + str(values[8]) + ' films)',
              '1990s (' + str(values[9]) + ' films)']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()

years = py_scraper(base_url, headers)
drawing(years)