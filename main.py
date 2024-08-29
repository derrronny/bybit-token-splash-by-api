import logging
import time
from time import sleep
from pybit import exceptions
from pybit.unified_trading import HTTP
import os

file = open('options.txt')

f = (file.readlines())

PROXY = 'http://' + f[0].split('-')[1].rstrip('\n')
API_KEY = f[1].split('-')[1].rstrip('\n')
SECRET_KEY = f[2].split('-')[1].rstrip('\n')
SYMBOL = f[3].split('-')[1].rstrip('\n')
COIN = f[4].split('-')[1].rstrip('\n')
BALANCE_FOR_TRADE = f[5].split('-')[1].rstrip('\n')
READY = 0

os.environ['http_proxy'] = PROXY
os.environ['HTTP_PROXY'] = PROXY
os.environ['https_proxy'] = PROXY
os.environ['HTTPS_PROXY'] = PROXY

file.close()


def round_down(value, decimals):
    factor = 1 / (10 ** decimals)
    return (value // factor) * factor


def token_splash():
    try:
        print(time)
        cl = HTTP(
            recv_window=60000, 
            api_key=API_KEY,
            api_secret=SECRET_KEY,
            max_retries=5,
        )
        p = cl.get_orderbook(
            category='spot',
            symbol=SYMBOL,
        )
        result = p['result']

        ask = result['a']
        ask_price = ask[0][0]
        print(ask_price)

        bid = result['b']
        bid_price = bid[0][0]
        print(bid_price)

        q = float(BALANCE_FOR_TRADE) / float(ask_price)
        quality = round(q, 0)
        print(quality)

        buy_order = cl.place_order(
            category='spot',
            symbol=SYMBOL,
            side='Buy',
            orderType='Limit',
            qty=quality,
            price=ask_price,
        )
        print('BUY')

        time.sleep(0.01)

        cv = cl.get_wallet_balance(
            accountType='UNIFIED',
            coin=COIN,
        )
        coin_value = cv['result']
        left = coin_value['list'][0]
        left_value = left['coin']
        wallet_balance = left_value[0]
        wall_before_round = float(wallet_balance['walletBalance'])

        sell_order = cl.place_order(
            category='spot',
            symbol=SYMBOL,
            side='Sell',
            orderType='Limit',
            qty=round_down(wall_before_round, 0),
            price=bid_price,
        )
        print('SELL')
        READY = 1

    except exceptions.InvalidRequestError as e:
        print('Bybit Request Error', e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print('Bybit Request Failed', e.status_code, e.message, sep=' | ')
    except Exception as e:
        print(e)


def main():
    token_splash()


if __name__ == '__main__':
    print('Wazzzup yosha')
    main()