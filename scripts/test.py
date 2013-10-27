import csv
with open("BBRY_2013-04-29.csv","rU") as f:
 	cf = csv.reader(f)
 	next(cf, None) # skip the header
 	for row in cf:
 		print row[0]



