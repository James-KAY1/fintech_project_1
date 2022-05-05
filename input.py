""" Input Application for Auto-Trader """

# Import required libraries
import sys
import fire
import questionary
from pathlib import Path
import os

# Function to input tickers to track as well as the buy and sell prices
def input_ticker_info():

    # Input ticker
    ticker = questionary.text("Please input your stock ticker").ask()

    # Input buy signal percentages
    buy_signal = questionary.text("What percentage would you like to use as your buy signal").ask()
    buy_signal = float(buy_signal)

    # Check that the percentage is positive
    if buy_signal < 0:
        buy_signal = questionary.text("Please enter a non-negative number").ask()

    # Ensure inputs are formatted to be consumed by auto-trader
    elif buy_signal > 0 and buy_signal < 1: 
        buy_signal = buy_signal
    else:
        buy_signal = buy_signal/100

    # Input sell signal percentages
    sell_signal = questionary.text("what percentage would you like to use as your sell signal").ask()
    sell_signal = float(sell_signal)

    # Check that the percentage is positive
    if sell_signal < 0:
        sell_signal = questionary.text("Please enter a non-negative number").ask()
    
    # Ensure unputs are formatted to be consumed by auto-trader
    elif sell_signal > 0 and sell_signal < 1:
        sell_signal = sell_signal
    else:
        sell_signal = sell_signal/100
    
    # Return variables
    print(ticker, buy_signal, sell_signal)
    return ticker, buy_signal, sell_signal

# Main function for running the script
def run():
    input_ticker_info()

if __name__ == "__main__":
    fire.Fire(run)