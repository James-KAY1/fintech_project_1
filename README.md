# AutoTrader Application
## Overview & Features
We are proud to showcase the development of an AutoTrader program that provides users who don't have the time and resource the research, analysis and trading capability through our fully-integrated Stock-Trading application.


This Application includes the following features:
1. Analysis and selection of the top performing tickers within the Technology, Energy, Health, Utility, and Finance sectors.
2. Command line interface with the application that users can utilize to select recommended tickers to trade.
3. The terminal interface will also offer the users the capablilities to select criterias for the buy/sell signals for the trading bot to use for placing trades on their behalf.

>![trading_bot](./Images/trading_bot.jpg)

---

## Technologies

Our AutoTrader Applicatoin utilizes  **Python (v 3.9.7)** and the following libraries:

`1.	fire    2. questionary   3. time  4. Path from pathlib  5. pandas  6. numpy 7. numpy.random 8. alpaca_trade_api
9.	REST, TimeFrame from alpaca_trade_api 10. load_dotenv from dotenv 11. requests 12. hvplot.pandas 13. sqlalchemy
14.	os 15. ast 16. json 17. requests_html 18. ftplib 19. yahoo.fin.stock_info 20. get_data from yahoo_fin.stock_info 
21.	IPython.display 22. io 23. matploblib.pyplot 24. mplot3d from mpl_toolkits 25. talib 26. websocket 27. plotly.graph_objects
28.	plotly.express`

---


## Installation Guide
Majority of the above libraries should be part of the base applications that were installed with the Python version above; if not, you will have to install them through the pip package manager of Python.

---
## Table of Contents
Please use the following links to access the different sections of the Repository/Application:

1. **Industry Sector ticker Analysis**:  Analysis and selection of tickers for each Industry Sector that will be recommended to user to trade (Utilizing Yahoo finance API & other libraries listed above).
   >[Technology](./Industry_sector_tickers_analysis/tech_stocks_analysis_selection.ipynb)
  
   >[Energy](./Industry_sector_tickers_analysis/energy_stocks_analysis_selection.ipynb)

   >[Health](./Industry_sector_tickers_analysis/health_stocks_analysis_selection.ipynb)

   >[Utility](./Industry_sector_tickers_analysis/utilities_stocks_analysis_selection.ipynb)

   >[Finance](./Industry_sector_tickers_analysis/finance_stocks_analysis_selection.ipynb)

1. **Command Line Interface (user) with Application**: Providing user the recommended ticker within each Industry sector listed above (Utilizing Fire and Questionary & other libraries listed above)


3. **Trading Bot**: Trading Bot that will place trades based on user's trading signal inputs utilzing a pull back trading strategy (Utilizing Alpaca API & other libraries listed above).


---

## Contributors
Contributors for the creation and deployment of the Autotrader Application and duties:

1. Ryan Anderson: a) Repo Owner b) Python Fire Function (Terminal functionality)
2. Tao Chen: a) Simple trading bot b) Real time data stream & stock technical analysis programming
3. James Handral: a)Industry sector tickers Data Collection, Clean up & Analysis  b) README file
4. Colton Mayes: a) Final Presentation b) Visualization for Presentation
5. Anton Maliksi: a) README file b) Final Presentation

---

## Licenses
No licenses were used for this project.