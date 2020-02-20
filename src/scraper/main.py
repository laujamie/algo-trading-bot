import requests
from bs4 import BeautifulSoup

# URL we use to scrape our NASDAQ-100 tickers
URL = 'https://en.wikipedia.org/wiki/NASDAQ-100'

if __name__ == '__main__':
    data = requests.get(URL)
    soup = BeautifulSoup(data.text, 'lxml')
    table = soup.find('table', {
        'class': 'wikitable sortable',
        'id': 'constituents'
    })

    tickers = []
    for row in table.findAll('tr')[1:]:
        try:
            ticker = row.findAll('td')[1].text
            tickers.append(ticker)
        except:
            print('Failed')

    with open('tickers.txt', 'w') as f:
        for ticker in tickers:
            f.write('%s' % ticker)

    print('Finished processing tickers')
