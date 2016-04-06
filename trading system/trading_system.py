import datetime
import math
import re
class TradingSystem(object):

	def __init__(self): 
		self.total_edge = 0

	#Function to fetch the sample data from the text file to be used in this project
	def get_data_dict(self):

		#Opening the file where sample data is located
		f = open('data.txt')
		data_array = []
		data_dict = {}
		for k in f.readlines():

			#splitting the information in the text file and converting to dictionary format for use
			data_array = re.split(r"\t+",k.replace("\n",""))
			key = data_array[0]+','+data_array[6]+','+data_array[7]
			data_dict[key]=data_array
		f.close()
		return data_dict

	def check_fun(self):
		return "working"

	#This function checks if the stock is present in the desired exchange
	@staticmethod
	def is_valid_symbol(sym,exc):
		valid_symbol="NYSE"
		
		if(sym == valid_symbol):
			return True
		else:
			return False

	#Retrieves available days for a given exchange value
	def get_days(self,exchange):
		days_arr = []
		raw_data = self.get_data_dict()
		for k in raw_data:
			if ((raw_data.get(k)[7])==exchange):
				days_arr.append((raw_data.get(k)[6]))
		return days_arr

	#Retrieves all the stocks and exchange for a given day
	def get_stocks(self,day):
		sym_arr = []
		raw_data = self.get_data_dict()
		for k in raw_data:
			if ((raw_data.get(k)[6])==day):
				sym_arr.append((raw_data.get(k)[0])+","+(raw_data.get(k)[7]))
		return sym_arr

	#Set the stocks which we request in future. This data is stored in stocks.txt separated by tab space
	def set_stocks(self,stocks):
		f = open('stocks.txt','w')
		for k in stocks:
			tmp = k.split(',')
			f.write(tmp[0]+'\t'+tmp[1]+'\n')
		f.close()

	#Function to return stock data in a dictionary format with symbol and day as inputs
	def get_stock_data(self,symbol,day):
		res_dict = {}
		raw_data = self.get_data_dict()
		tmp = symbol.split(',')
		symbol = tmp[0]
		for k in raw_data:
			if ((raw_data.get(k)[6])==str(day)):
				if ((raw_data.get(k)[0])==symbol):
						res_dict['symbol']=raw_data.get(k)[0]
						res_dict['close']=raw_data.get(k)[1]
						res_dict['high']=raw_data.get(k)[2]
						res_dict['low']=raw_data.get(k)[3]
						res_dict['open']=raw_data.get(k)[4]
						res_dict['exchange']=raw_data.get(k)[7]
		return res_dict

	#Function to analyse the stock object passed to it and stores in stock_result.txt
	def set_stock_param(self,obj):
		#print "in set param"
		#print obj.symbol
		sym = obj.symbol.split(',')[0]
		exc = obj.symbol.split(',')[1]

		#passing some current value related to the price of the symbol for program testing purpose
		if(obj.symbol.split(',')[0]=='IBM'):
			edge = obj.get_edge(54)
		else:
			edge = obj.get_edge(148)
		f = open('stock_result.txt','a')
		f.write(sym+"\t"+exc+"\t"+str(edge[0])+"\t"+str(edge[1])+"\n")
		f.close()
		self.set_total_edge(edge[0])

	#Function to calculate the total edge value. This result is printed to console. This value is modified from
	#iteration to iteration and final value is the total edge for all the analysed stocks
	def set_total_edge(self,value):
		self.total_edge = self.total_edge + value

#Stock class for storing the symbol and getting edge value for the stock. Object created for this class will be
#passed to set_stock_param for the analysis part
class StockClass(object):
	from trading_system import TradingSystem
	def __init__(self, symbol): 
		self.symbol = symbol

	#Function to calculate the edge
	def get_edge(self,currentprice):
		tk = TradingSystem()
		i=1
		sum_price = 0
		sum_diff_price = 0
		while(i<=10):

			#Calculating the stock data for last ten days from todays date
			temp_dict =  tk.get_stock_data(self.symbol,int(str(datetime.date.today()-datetime.timedelta(i)).replace('-','')))
			j=0

			#Trying to fetch the data when high < low. This continues for 5 attempts
			while(j<5):
				if(temp_dict.get('low')<temp_dict.get('high')):
					break
				else:
					temp_dict =  tk.get_stock_data(self.symbol,int(str(datetime.date.today()-datetime.timedelta(i)).replace('-','')))
				j=j+1

			#adding the difference of current price and closing price
			diff = float(currentprice)-float(temp_dict.get('close'))
			sum_price = sum_price + diff
			sum_diff_price = sum_diff_price + (diff**2)
			i=i+1

		#calculating mean of the differences 
		edge =  float(sum_price/10)

		#calculating standard deviation
		sd = float(math.sqrt(sum_diff_price/10))
		tk.set_total_edge(edge)
		return edge,sd

