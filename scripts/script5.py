import csv #imports csv file from system
c = csv.writer(open("BBRY_2013-04-29.csv","wb"))# function csv.writer open the file BBRY csv file and writes it
c.writerow(["Time","Close","High","Low","Open","Volume"])

cr = csv.reader(open("BBRY_2013-04-29.csv","rb"))
for row in cr:
	print row

