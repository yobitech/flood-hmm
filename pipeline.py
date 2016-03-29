
import MySQLdb
import numpy as np
import pandas as pd

# full pipeline
def pipeline():

	n_predict = 3
	n_times = 2
	n_rows = 100
	n_back = 10
	
	############################

	# 1. get data from both sources

	# yobi: last_updated, rainfall
	ws_data = get_data('ws10', ['last_updated', 'rainfall'], n_rows)

	# accuweather: last_updated, (rf, pct)*(1,2,3)
	# assuming the format is: (days predicted)+'aw'+(measurement)+(timeofday)
	# results in: 1awrf1, 1awrf2, 2awrf1, 2awrf2, 3awrf1, 3awrf2, ...
	aw_cols = []
	measurements = ['rf', 'pct']
	for measurement in measurements: 
		for i in range(1, n_predict+1):
			for j in range(1, n_times+1):
				aw_cols.append(str(i) + 'aw' + measurement + str(j))
	aw_data = get_data('ws10', ['last_updated'] + aw_cols, n_rows)

	############################

	# 2. format data
	ws_df = pd.DataFrame(ws_data)
	aw_df = pd.DataFrame(aw_data)

		# end with: 
		# yobi: date, measured value
			# sum/average all of the rainfalls for a given day
			# condense the date to the given day
		# accuweather: date, days ahead, rf, pct
		# make sure that the last measured days are the same!!!

	############################

	# 3. calculate the errors for each set
	errors = []

	# for each of the days ahead,
	for i in range(1, n_predict+1):
		actual = get_col(ws_df, [0, n_back])
		predicted = get_col(aw_df, [n_predict, n_predict+n_back], n_predict=n_predict)
		# check against actual
		errors.append(calc_r2(actual, predicted))

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

def get_col(source, range, n_predict=-1):

	# return numpy array
	pass


def calc_r2(actual, predicted):

	# assumming the passed in arrays are numpy

	actual_mean = sum(actual)/len(actual)
	ss_res = sum(pow(actual-predicted, 2))
	ss_tot = sum(pow(acutal-actual_mean, 2))

	return 1-ss_res/ss_tot

