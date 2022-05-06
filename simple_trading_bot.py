# Import required libraries
import os
import alpaca_trade_api as tradeapi
import time
from dotenv import load_dotenv

from input import input_ticker_info

# Load env file and connect to Alpacas API
load_dotenv('api.env')
alpaca_api_key = os.getenv('ALPACA_API_KEY')
alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')

# Create alpacas API object
api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, "https://paper-api.alpaca.markets", "v2")

# Set ticker variables
ticker = input_ticker_info.ticker
buy_signal = input_ticker_info.buy_signal
sell_signal = input_ticker_info.sell_signal

# Initialize trading bot
while True:
    try:
        api.get_position(ticker)
        time.sleep(11)
    except:
        api.submit_order(symbol=ticker,qty=1,side='buy',type='market',time_in_force='gtc')
        time.sleep(10)
        api.submit_order(symbol=ticker,qty=1,side='sell',type='trailing_stop',trail_percent=sell_signal,time_in_force='gtc')