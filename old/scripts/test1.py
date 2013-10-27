import csv


cr = csv.reader(open("copy.csv","rU"))
c1 = []
for row in cr:
	c1.append(row[0])
	print row[0]
	