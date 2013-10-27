output =[]

f = open("BBRY_2013-04-29.csv","rU")
for line in f:
	cells = line.split(",")
	output.append((cells[1]))# only writing time and close
	
f.close()
print output