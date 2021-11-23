import requests
import pandas as pd
import os

API_KEY = os.environ.get('TRADIER_KEY')  # '1P9ggGodGMtq7jZAGLZxs6Ad8N3M'
API_URL = "https://sandbox.tradier.com/v1/"
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}
target_url = API_URL + "markets/options/chains"


def getOptions(ticker='AAPL',
               expiry_date="2021-12-17", type='put'):

    params = dict(symbol=ticker, expiration=expiry_date, greeks='true')
    r = requests.get(target_url, params=params, headers=HEADERS)

    options = pd.json_normalize(
        r.json()['options']['option'])
    options['lastPrice'] = options['last']
    options['openInterest'] = options['open_interest']
    options['delta'] = abs(options['greeks.delta'])*100
    filter = options['option_type'] == type
    options = options[filter]
    return (options[["strike",
                    "lastPrice",
                     'delta',
                     "openInterest",
                     ]])
