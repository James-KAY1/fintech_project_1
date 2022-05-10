""" Input Application for Auto-Trader """

# Import required libraries
# TEST ignore api.evv
# Test2 
#test 3
import fire
import questionary
import time
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import ast
import json
#import requests
#import talib as ta
import websocket
from alpaca_trade_api import REST, TimeFrame
#import alpaca_trade_api as tradeapi
#from dotenv import load_dotenv
#import os
from utils.helper import get_alpacas_info

alpaca_api_key = get_alpacas_info()[2]
alpaca_secret_key = get_alpacas_info()[3]

#load_dotenv('api.env')
#alpaca_api_key = os.getenv('ALPACA_API_KEY')
#alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')
#type(alpaca_secret_key)

# Function to input tickers to track as well as the buy and sell prices
def input_ticker_info():
    # Import csv
    sectors_and_tickers = pd.read_csv(
        Path("./Resources/sectors_and_tickers.csv")
    )

    # Set the sectors available for selection based on columns in CSV
    sector_list = sectors_and_tickers.columns

    # Select the sector for the stock you would like to trade
    sector = questionary.select("From which sector would you like to select your stock?",choices=sector_list).ask()

    # Assign the list of avaible tickers based on the sector selected
    ticker_list = sectors_and_tickers[f"{sector}"]

    # Select the ticker you would like to trade
    ticker = questionary.select("Please select the ticker you would like to trade.",choices=ticker_list).ask()

    # Get current buying power
    buying_power = get_alpacas_info()[0].buying_power
    buying_power = float(buying_power)

    print(f"You have {buying_power} to trade.")

    # Input percentage of portfolio to allocate to this stock
    allocation = questionary.text(f"What percentage of your cash on hand would you like to allocate to trading {ticker} ?").ask()
    allocation = float(allocation)

    # Check that the percentage is positive and not above 100%
    if allocation < 0:
        allocation = questionary.text("Please enter a non-negative number").ask()
    elif allocation > 100:
        allocation = questionary.text("Please enter a number less than 100").ask()

    allocation = float(allocation)
    
    # Ensure inputs are formatted to be consumed by auto-trader
    if allocation > 0 and allocation < 1: 
        allocation = allocation
    else:
        allocation = allocation/100

    # Assign amount to allocate to stock
    trade_allocation = allocation * buying_power

    # Input buy signal percentages
    process_buy = True
    while process_buy:
        buy_signal = questionary.text("What percentage would you like to use as your buy signal").ask()
        buy_signal = float(buy_signal)

        # Handle zero value entries    
        if buy_signal == 0:
            buy_opt_out = questionary.confirm("Are you sure you do not want to buy any of these shares today?").ask()
            if buy_opt_out:
                break
            else:
                continue
        break

    # Ensure inputs are formatted to be consumed by auto-trader
    if buy_signal > 0 and buy_signal < 1: 
        buy_signal = buy_signal
    else:
        buy_signal = buy_signal/100

    # Input sell signal percentages
    process_sell = True
    while process_sell:
        sell_signal = questionary.text("what percentage would you like to use as your sell signal").ask()
        sell_signal = float(sell_signal)

        # Check that the percentage is positive
        if sell_signal < 0:
            sell_signal = questionary.text("Please enter a non-negative number").ask()
        # Handle zero value entries 
        elif sell_signal == 0:
            sell_opt_out = questionary.confirm("Are you sure you do not want to buy any of these shares today?").ask()
            if sell_opt_out:
                break
            else:
                continue
        break
    
    # Ensure unputs are formatted to be consumed by auto-trader
    if sell_signal > 0 and sell_signal < 1:
        sell_signal = sell_signal
    else:
        sell_signal = sell_signal/100
    
    # Return variables
    print(ticker, buy_signal, sell_signal, trade_allocation)
    return ticker, buy_signal, sell_signal, trade_allocation

def run_robo_trader(ticker, buy_signal, sell_signal, trade_allocation):
    # Initialize trading bot
    # extract 10 days prior price 
    days_to_subtract = 11
    today = (datetime.today()).strftime('%Y-%m-%d')
    print(f'today is {today}')
    earlier_date_to_compare = (datetime.today()-timedelta(days=days_to_subtract)).strftime('%Y-%m-%d')
    print(f'earlier_date_to_compare is {earlier_date_to_compare}')

    # Extract price of earlier date from Alpaca API
    #rest_client = REST(alpaca_api_key, alpaca_secret_key)
    #bars_from_earlier_date = rest_client.get_bars(ticker, TimeFrame.Day, earlier_date_to_compare, earlier_date_to_compare).df

    bars_from_earlier_date = get_alpacas_info()[1].get_bars(ticker, TimeFrame.Day, earlier_date_to_compare, earlier_date_to_compare).df
    print(f'bars_from_earlier_date {bars_from_earlier_date}')
    price_from_earlier_date = bars_from_earlier_date.iloc[0]['close']
    print(f'The price_from_earlier_date is {price_from_earlier_date}')
    
    # Calculating trading signal
    price_to_start_trading_bot = price_from_earlier_date * (1+buy_signal)
    print(f'price_to_start_trading_bot is {price_to_start_trading_bot}')
    
    # link for alcapa socket 
    socket = "wss://stream.data.alpaca.markets/v2/iex"

    # Define functions for websocket
    def on_open(ws):
        print("opened")
        auth_data = {"action":"auth","key":alpaca_api_key,"secret":alpaca_secret_key}
        ws.send(json.dumps(auth_data))
        listen_message = {"action":"subscribe","bars":[ticker]}
        ws.send(json.dumps(listen_message))


    def on_message(ws, message):
        print("received a message")
        print(message)
        formatted_message = ast.literal_eval(message)
        last_time = formatted_message[0].get("t")
        last_close = formatted_message[0].get("c")
        print(f'infor from previous minute: time is {last_time}; close is {last_close};')
        shares_to_trade = trade_allocation//last_close
    # Once the realtime price exceeds the signal price, start the trading bot
        if last_close>price_to_start_trading_bot:
            print(f'Buy signal price {price_to_start_trading_bot} has just been reached, starting the Trading Bot...')
            while True:
                try:
                    get_alpacas_info()[1].get_position(ticker)
                    time.sleep(11)
                except:
                    get_alpacas_info()[1].submit_order(symbol=ticker,qty=shares_to_trade,side='buy',type='market',time_in_force='gtc')
                    time.sleep(10)
                    get_alpacas_info()[1].submit_order(symbol=ticker,qty=shares_to_trade,side='sell', type='trailing_stop', trail_percent=sell_signal, time_in_force='gtc')

    def on_close(ws):
        print("closed connection")

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

# Main function for running the script
def run():
    ticker, buy_signal, sell_signal, trade_allocation = input_ticker_info()
    run_robo_trader(ticker, buy_signal, sell_signal, trade_allocation)

if __name__ == "__main__":
    fire.Fire(run)
