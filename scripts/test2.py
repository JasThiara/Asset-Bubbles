import csv
import math
cr = csv.reader(open("BBRY_2013-04-29.csv","rU"))
c1 = []
for row in cr:
	c1.append(row[1])
	print row[1]
	s = row[1] #not needed
def stddev(s):
	m= mean(s)
	sumsq = 0.0
	for i in range (len(s)):
		sumsq += (s[i]-m)**2 #Right hand side (RHS) should be(x[i]- m)**2
	return math.sqrt(sumsq/len(s)) #RHS should be math.sqrt(sumsq/len(s))
	print "testing stddev: "
	print stddev([1,2,3,4])#do this one by hand to make sure your 
	print "\n"
	print "actual stddev: "
	print stddev(c1)

