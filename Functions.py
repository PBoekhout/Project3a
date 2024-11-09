import requests
import os
import pygal
import lxml

#apikey = "FVQDMTI5GIVCHLQT"

apikey = os.environ.get('FVQDMTI5GIVCHLQT')

def TIME_SERIES_INTRADAY(symbol, interval):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&apikey={apikey}&outputsize=full'
    r = requests.get(url)
    data = r.json()
    return data

def TIME_SERIES_DAILY(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}&outputsize=full'
    r = requests.get(url)
    data = r.json()
    return data

def TIME_SERIES_WEEKLY(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    return data

def TIME_SERIES_MONTHLY(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    return data
