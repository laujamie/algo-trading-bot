# Algorithmic Trading Bot

An algorithmic trading bot created in Python to trade distressed stocks and **`QQQ`**.

Original algorithm used here can be found on [Medium](https://medium.com/automation-generation/how-to-trade-distressed-stocks-using-free-apis-dd7f43e9be33).

## Usage

Assuming you are on a UNIX system, run the following in the project base folder:

```bash
pip3 install --upgrade pipenv  # Skip this if you have pipenv
pipenv install
pipenv shell

export TENQUANT_API="<YOUR TENQUANT API KEY>"
export ALPACA_API="<YOUR ALPACA API KEY>"
export ALPACA_SECRET="<YOUR ALPACA SECRET KEY>"

python3 src/scraper/main.py
python3 src/bot/main.py
```
