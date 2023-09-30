from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

def get_coin_id_from_symbol(symbol):
    coins_list = cg.get_coins_list()
    for coin in coins_list:
        if coin['symbol'] == symbol.lower():
            return coin['id']
    return None

def get_price_from_symbol(symbol):
    coin_id = get_coin_id_from_symbol(symbol)
    if coin_id:
        coin_data = cg.get_price(coin_id)
        return coin_data['market_data']['current_price']['usd']
    else:
        return None