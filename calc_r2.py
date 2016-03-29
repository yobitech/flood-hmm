import numpy as np
import math
import pandas as pd
# import MySQLdb

def pipeline(n_rows, measurements, n_predict, n_back):

  # get the data
  # determine which data to get
  aws = get_data('aws', n_rows, measurements, n_predict)
  wso = get_data('wso', n_rows, measurements, n_predict)

  # calc errors for each instance
  errors = []

  for measurement in measurements:
    # for time in ['morn', 'night']:
    for time in range(1,3):
      errs = calc_errors(predicted, observed, n_predict, n_back, 0)
      errors.append({
        'measurement': measurement,
        'time_of_day': time,
        'vals': errs
      })
      # calc_errors(predicted, observed, n_predict, n_back, t)
    # print the errors
    print errors
    return errors

def test_pipeline():


  measurements = ['rf', 'pct', 'ws']
  measurements_ws = ['air_temp1', 'air_temp2', 'humdity', 'wind_speed', 'air_pressure', 'solar_radiation']
  n_rows = 20
  n_back = 10
  n_predict = 3



def get_data(source, n_rows, measurements, n_predict):

  data = []

  # connect to database
  # db = MySQLdb.connect('localhost','root','yobi1234','myvillageshop_logins')
  # cursor = db.cursor()

  if source == 'aws':
    # get the table information
    query = 'SELECT (last_update,'
    for measurement in measurements:
      for i in range(1, n_predict+1):
        for j in range(1,3):
          query += str(i) + 'aw' + measurement + str(j) + ','
    query = query[:-1]
    query += ') FROM ws10'
    print query
    # cursor.execute(query)

    # get up to n_rows rows
    for n in range(n_rows):
      row = cursor.fetchone()
      for i in range(1, n_predict+1):
        for j in range(1,3):
          col = str(i) + measurement + str(j) + ','
          data.append({
            'date': d,
            'measurement': measurement, 
            'time_of_day': j,
            'n_predict': i,
            'value': row[col]
          })

  elif source == 'wso':

    # get table information 
    query = 'SELECT (last_update,'
    for measurement in measurements:
      query += measurement + ','
    query = query[:-1]
    query += ') FROM x'
    print query
    # cursor.execute(query)

    # get up to n_rows rows
    for n in range(n_rows):
      row = cursor.fetchone()
      data.append({'date': d, 'value': row['v']})

  return pd.DataFrame(data)

def test_data():

  get_data('wso', 0, ['rf', 'pct', 'winds', 'precip'], 3)

test_data()


def calc_errors(predicted, observed, n_predict, n_back, t):

  errors = []

  for p in range(1, n_predict+1):

    # print p, t, t+p, n_back, p
    predicted_set = get_predicted(predicted, t+p, n_back, p)
    observed_set = get_observed(observed, t, n_back)
    # print predicted_set, observed_set

    diffs = calc_diff(predicted_set, observed_set)
    # print diffs 
    errors.append(calc_mae(diffs))

  return errors

def calc_diff(a, b):
  return [ai-bi for ai,bi in zip(a,b)]


def calc_mae(errors):
  return sum([abs(e) for e in errors])/len(errors)

def calc_rmse(errors):
  return math.sqrt(sum([pow(e,2) for e in errors])/len(errors))

def get_predicted(predicted, t_start, n_back, p):
  return predicted[p][t_start:t_start+n_back]

def get_observed(observed, t_start, n_back):
  return observed[t_start:t_start+n_back]

def test():

  predicted = [[9, 9, 9, 9, 9, 9, 9, 9], [0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7]]
  observed = [3, 4, 5, 6, 7, 8, 9, 10]

  print calc_errors(predicted, observed, 3, 3, 0)

# test()