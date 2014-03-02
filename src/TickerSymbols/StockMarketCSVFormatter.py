'''
Created on Mar 2, 2014

@author: Jas
'''
import csv
if __name__ == '__main__':
    isNYSE = False
    if isNYSE:
        readMe = open('NYSE.txt','r')
        writeMe = open('NYSE.csv','w')
    else:
        readMe = open('NASDAQ.txt','r')
        writeMe = open('NASDAQ.csv','w')
    csvFileReader = csv.reader(readMe, delimiter='	')
    csvFileWriter = csv.writer(writeMe,delimiter=',')
    for row in csvFileReader:
        csvFileWriter.writerow(row)
    