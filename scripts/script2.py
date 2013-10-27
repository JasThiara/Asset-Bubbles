import ystockquote

import datetime

from sys import argv

script, symbol, price, time = argv
 
def get_price_time(symbol):
	price = ystockquote.get_price(symbol)
	current_time = datetime.datetime.now()
	print [price, current_time]

import sched, time

s = sched.scheduler(time.time, time.sleep)
print time.time()
i = 0

while i<= 60:
	s.enter(i, 1, get_price_time, (symbol,))
	i = i+10
	
s.run()