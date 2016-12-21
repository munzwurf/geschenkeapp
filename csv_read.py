import csv

with open ('geschenke.csv') as csvfile:
	reader = csv.reader(csvfile)
	reader.next()
	for row in reader:
		#print "Row:" + ",".join(row)
		print row