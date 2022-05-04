""" Input Application for Auto-Trader """

# Import required libraries
import sys
import fire
import questionary
from pathlib import Path
import os

# Function to input tickers to track as well as the buy and sell prices
def input_ticker_info():

    # Prompts for ticket input, as well as buy and sell signals
    ticker = questionary.text("Please input your stock ticker").ask()
    buy_signal = questionary.text("What percentage would you like to use as your buy signal").ask()
    buy_signal = float(buy_signal)

    # Check that the percentage is positive
    if buy_signal < 0:
        buy_signal = questionary.text("Please enter a non-negative number").ask()

    sell_signal = questionary.text("what percentage would you like to use as your sell signal").ask()
    sell_signal = float(sell_signal)

    # Check that the percentage is positive
    if sell_signal < 0:
        sell_signal = questionary.text("Please enter a non-negative number").ask()
    
    # Return variables
    print(ticker, buy_signal, sell_signal)
    return ticker, buy_signal, sell_signal

def run():
    input_ticker_info()

if __name__ == "__main__":
    fire.Fire(run)