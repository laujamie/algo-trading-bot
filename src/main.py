import os
import requests
import json
import alpaca_trade_api as tradeapi

from scraper import get_tickers

base_url = 'https://paper-api.alpaca.markets'
tenquant_base_url = 'https://api.tenquant.io'

if __name__ == '__main__':
    tickers = []

    with open('tickers.txt', 'r+') as f:
        tickers = f.read().splitlines()

    if len(tickers) == 0:
        get_tickers()
        with open('tickers.txt', 'r+') as f:
            tickers = f.read().splitlines()

    tenquant_api = os.environ['TENQUANT_API']

    key = os.environ['ALPACA_API']
    secret = os.environ['ALPACA_SECRET']
    api = tradeapi.REST(key, secret, base_url, api_version='v2')
    clock = api.get_clock()
    account = api.get_account()

    if not clock.is_open:
        print('Market closed, exiting now...')
        exit

    all_stocks_data = {}
    print('Retrieving stock data...')
    for ticker in tickers:
        print('Processing {}'.format(ticker))
        params = {'ticker': ticker, 'key': tenquant_api}
        req_json = requests.get(tenquant_base_url + '/data',
                                params=params).content
        try:
            stock_data = dict(json.loads(req_json))
        except:
            continue
        if 'error' in stock_data.keys():
            continue

        current_assets = stock_data['currentassets']
        current_liabilities = stock_data['currentliabilities']

        current_ratio = current_assets / current_liabilities

        all_stocks_data[ticker] = current_ratio

    all_stocks_data = sorted(all_stocks_data.items(), key=lambda x: x[1])

    shorts = all_stocks_data[:len(all_stocks_data) // 5 + 1]
    print('Shorts:')
    print(shorts)

    weightings = {}
    portfolio_value = float(account.portfolio_value)
    for stock, current_ratio in shorts:
        price = api.get_barset(stock, "minute", 1)[stock][0].c
        weightings[stock] = -((portfolio_value / 2) / len(shorts)) / price
    qqq_price = api.get_barset('QQQ', "minute", 1)['QQQ'][0].c
    weightings['QQQ'] = (portfolio_value / 2) / qqq_price

    for short_stock in weightings.keys():
        qty = int(weightings[short_stock])
        if qty < 1:
            side = 'sell'
        else:
            side = 'buy'
        qty = abs(qty)
        # place orders
        try:
            api.submit_order(short_stock, qty, side, "market", "day")
            print("Market order of | " + str(qty) + " " + short_stock + " " +
                  side + " | completed.")
        except:
            print("Order of | " + str(qty) + " " + short_stock + " " + side +
                  " | did not go through.")
