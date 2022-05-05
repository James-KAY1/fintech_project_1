""" Input Application for Auto-Trader """

# Import required libraries
import fire
import questionary
from pathlib import Path
import os

from utils.helper import get_alpacas_info

# Function to input tickers to track as well as the buy and sell prices
def input_ticker_info():

    # Input ticker
    ticker = questionary.text("Please input your stock ticker").ask()

    # IF WE START TO ITERATE THROUGH STOCKS, (I.E ADDING MORE THAN 1) WE WILL NEED THE ABILITY TO DEDUCT THE TRADE ALLOCATIONS FROM THE TRADE BALANCE
    # Get current buying power
    buying_power = get_alpacas_info().buying_power
    buying_power = float(buying_power)

    print(f"You have {buying_power} to trade.")

    # Input percentage of portfolio to allocate to this stock
    allocation = questionary.text(f"What percentage of your cash on hand would you like to allocate to trading {ticker} ?").ask()
    allocation = float(allocation)

    # Check that the percentage is positive
    if allocation < 0:
        allocation = questionary.text("Please enter a non-negative number").ask()

    # Ensure inputs are formatted to be consumed by auto-trader
    elif allocation > 0 and allocation < 1: 
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

# Main function for running the script
def run():
    input_ticker_info()

if __name__ == "__main__":
    fire.Fire(run)
