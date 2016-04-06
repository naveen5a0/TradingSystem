# TradingSystem
Sample trading system which accepts exchange at command line
About this system
-----------------------
This system accepts exchange ("NYSE") at command line and prints the analysis of all the stocks such as the edge values,mean, standard deviation.
This system first lists the all stocks in the given exchange and picks the current price based on the recent valid day available and compares with
the price of the stock for the past ten days and calculates mean,standard deviation , edge values, total edge and stores the analysis in 
stock_result.txt and also prints to console.This system eliminates weekends which are not valid in real time trading system.
Currently this program is operating on test data data.txt

Files information
----------------
main.py - main python file
tradingsystem.py - this file contains all the classes and methods required
data.txt - input data for this script
stocks.txt - list of future stocks
stock_result.txt - analysis of the stocks

Execution
-----------
python main.py NYSE
