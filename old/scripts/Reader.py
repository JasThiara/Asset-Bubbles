# It is not printing x values and sigma(x) like before
#from sage.all import *
import csv
from Sublocaltime import *
def is_number(rowValue):
	''' Please use/call this method in your script below to determine if row[1] is a numerical string or not.'''
	try:
		float(rowValue)
		return True
	except ValueError:
		return False
cr = csv.reader(open("BBRY_2013-04-29.csv","r U"))
next(cr, None) # skip the header

c1 = []

for row in cr: # reading file from csv file	
	if is_number(row[1]):#if the string, row[1], is a numerical string 
		c1.append(float(row[1]))#add it into the list.
n = len(c1)
h_n= Derive_hn(c1)
T = 60*n
x = Derive_x_values(c1)
Sigma = [Volatility_estimation(T,c1,ex,n,h_n) for ex in x]
print  x
print  Sigma
