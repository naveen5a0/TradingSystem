from trading_system import TradingSystem
from trading_system import StockClass
import sys
import datetime

'''
Sample stocks related data present in data.txt. This script uses that data for testing and printing the result.
future Stock list (i.e) the function set_stocks stores the stocks list in stocks.txt
Analysis of the stocks are stored in stocks_result.txt. They are stored in symbol,Exchange,edge value,standard deviation
separated by tab space.
This data.txt file will be applicable till 14-april as the stock data is included till april 14 for testing purpose
'''

#Creating an object for the TradingSystem Class
trs = TradingSystem()

#Passing the Exchange value to retrieve list of days available
dates_array = trs.get_days(str(sys.argv[1]))
#Eliminating duplicates
dates_array = list(set(dates_array))
weekdays_arr = []

#Removing the Weekends from the days list
for k in dates_array:
	weekday = datetime.date(int(k[0:4]),int(k[4:6]),int(k[6:8])).weekday()
	if(int(weekday)==5)or(int(weekday)==6):
		pass
	else:
		weekdays_arr.append(k)

#Calculating the most recent date from the fetched days information from previous result
recent_date = max(weekdays_arr)

#List of stocks on the recent available day
stocks_array = trs.get_stocks(recent_date)

#Passing the stocks array to set stocks function for future
trs.set_stocks(stocks_array)

#setting attibute names in stock_result.txt. This file will be used to store stock analysis
f = open('stock_result.txt','w')
f.write("symbol\texchange\tedge\tstandarddev\n")
f.close()

'''
Picking Each stock at a time and creating an object of StockClass type which contains a symbol attribute
and get_edge function
'''

for i in stocks_array:
	tmp=i.split(',')

	#Checking if the Exchange is the desired one and then passing the Symbol
	if(TradingSystem.is_valid_symbol(tmp[1],tmp[0])):

		#Creating the object for the symbol
		k=StockClass(i)

		#Passing the stock object created to set stock param function
		trs.set_stock_param(k)

print "Total Edge Value is"
print trs.total_edge
print "Edge values and standard deviation for stocks\n"
f=open('stock_result.txt')
for k in f.readlines():
	print k
f.close()
print "*Analysis Regarding the stocks are saved in stock_result.txt file located in the current directory"
