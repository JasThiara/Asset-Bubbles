import ystockquote # going to ystockquote 

import sched, time, datetime # to recieve scheduler, time and datetime

from sys import argv # from system get argument variable

script, symbol, start_specific_time, end_specific_time, filename, datarate = argv

def get_price_time(symbol):
	price = ystockquote.get_price(symbol)
	current_time = datetime.datetime.now()
	return [symbol, price, str(current_time)]
	
def create_file(filename):
	return open(filename,'w')

def close_file(target):
	target.close()
	
def write_data_to_file(target, data):
	target.write(data[0])# first element of list which is symbol
	target.write(",")
	target.write(data[1])# 2nd element of list which is price
	target.write(",")
	target.write(str(data[2])) # 3rd element date which is string
	target.write ("\n") # create new line 
	
def input_datetime_convertor(time_string): # creating function which will convert start_specific_time to datetime
	year=int(time_string[0:4])
	month = int(time_string[4:6])
	day= int(time_string[6:8])
	hour = int(time_string[8:10])
	minute = int(time_string[10:12])
	seconds = int(time_string[12:14])
	input_datetime = datetime.datetime(year,month,day,hour,minute,seconds)
	return input_datetime

def delta_time(later_datetime):
	current_datetime = datetime.datetime.now()
	delta =input_datetime_convertor(later_datetime)-current_datetime
	return delta.seconds

def sleep(later_datetime):
	time.sleep(delta_time(later_datetime))
	

def get_additional_data(symbol,datalist):
	new_data = get_price_time(symbol)
	datalist.append(new_data)
	
	
def build_scheduler(datarate, start_time, end_time,symbol,datalist):
	s = sched.scheduler(time.time, time.sleep)
	print time.time()
	seconds = datetime.timedelta(0,int(datarate))
	k = input_datetime_convertor(start_time)
	i =input_datetime_convertor(start_time)# we need to pass time through convertor so it will be in string
	while i<=input_datetime_convertor(end_time):
		s.enter((i-k).seconds, 1,get_additional_data, (symbol,datalist))
		print (i-k).seconds
		i = i+seconds	
	s.run()
	
def csv_file_generator(filename,Data):
	target = open(filename,'w')
	for item in Data:
		for element in item:
			target.write(element)
			target.write(",")
		target.write("\n")
	target.close()
		
		
sleep(end_specific_time)
datalist = list()
build_scheduler(datarate, start_specific_time, end_specific_time,symbol,datalist)
csv_file_generator(filename,datalist)		