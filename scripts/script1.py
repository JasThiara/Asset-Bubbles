import ystockquote

from sys import argv

script, symbol, start_date, end_date,filename = argv

Data = ystockquote.get_historical_prices(symbol, start_date, end_date)


target = open(filename,'w')

for item in Data:
	for element in item:
		target.write(element)
		target.write(",")
	target.write("\n")
