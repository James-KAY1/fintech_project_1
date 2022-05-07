""" Input Application for Auto-Trader """

# Import required libraries
import fire
import questionary
import time
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

from utils.helper import get_alpacas_info

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

        # Check that the percentage is positive
        if buy_signal < 0:
            buy_signal = questionary.text("Please enter a non-negative number").ask()

        # Handle zero value entries    
        elif buy_signal == 0:
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
    while True:
        try:
            get_alpacas_info()[1].get_position(ticker)
            time.sleep(11)
        except:
            get_alpacas_info()[1].submit_order(symbol=ticker,qty=1,side='buy',type='market',time_in_force='gtc')
            time.sleep(10)
            get_alpacas_info()[1].submit_order(symbol=ticker,qty=1,side='sell', type='trailing_stop', trail_percent=sell_signal, time_in_force='gtc')

# Main function for running the script
def run():
    ticker, buy_signal, sell_signal, trade_allocation = input_ticker_info()
    run_robo_trader(ticker, buy_signal, sell_signal, trade_allocation)

if __name__ == "__main__":
    fire.Fire(run)
