
import MySQLdb
import numpy as np

# full pipeline
def pipeline():

	n_predict = 3
	n_times = 2
	
	############################

	# 1. get data from both sources

	# yobi: last_updated, rainfall
	ws_data = get_data('ws10', ['last_updated', 'rainfall'], 100)

	# accuweather: last_updated, (rf, pct)*(1,2,3)
	# assuming the format is: (days predicted)+'aw'+(measurement)+(timeofday)
	# results in: 1awrf1, 1awrf2, 2awrf1, 2awrf2, 3awrf1, 3awrf2, ...
	aw_cols = []
	measurements = ['rf', 'pct']
	for measurement in measurements: 
		for i in range(1, n_predict+1):
			for j in range(1, n_times+1):
				aw_cols.append(str(i) + 'aw' + measurement + str(j))
	aw_data = get_data('ws10', ['last_updated'] + aw_cols, 100)

	############################

	# 2. format data

		# end with: 
		# yobi: date, measured value
			# sum/average all of the rainfalls for a given day
			# condense the date to the given day
		# accuweather: date, days ahead, rf, pct

	############################

	# 3. calculate the errors for each set
	errors = []

	# for each of the days ahead,
	for i in range(1, n_predict+1):
		# check against actual

	############################

	# 4. return errors
	return errors

def get_data(source, columns, n_rows):

	data = []

	# connect to database
	db = MySQLdb.connect('localhost','root','yobi1234','myvillageshop_logins')
	cursor = db.cursor()

	# build query
	query = 'SELECT (' + ','.join(columns) 
		+ ') FROM ' + source + ' LIMIT ' + n_rows
	cursor.execute(query)

	results = cursor.fetchall()

	# disconnect from server
	db.close()

	return results

def calc_r2(actual, observed):

	# assumming the passed in arrays are numpy

	# SSres <- sum((I-Isim)^2)
	# SStot <- sum((I-mean(I))^2)
	# Rsq <- 1 - SSres/SStot
	actual_mean = sum(actual)/len(actual)
	ss_res = sum(pow(actual-observed, 2))
	ss_tot = sum(pow(acutal-actual_mean, 2))

	return 1-ss_res/ss_tot

