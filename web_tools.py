import requests
def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        adress = requests.get(url).json()
        btc = adress["bitcoin"]["usd"]
        return f"the lastst price of BTC is : {btc} "
    except:
        return 65000.0

