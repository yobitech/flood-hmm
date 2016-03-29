import pandas as pd 
import numpy as np 

def calc_confidence(prediction, actual, n_predict, n_back, t):

  all_errs = []

  # look at the past 10 days
  for b in range(n_back):
    # print 'b', b

    # calculate the errors
    for n in range(n_predict):

      # print 'n', n
      errs = []
      # number of days back, assuming that T=0 is present
      b_back = (b+n_predict) 
      print b, n, b_back, get_predict(prediction, t, b_back, n), get_actual(actual, t, b_back-n)
      errs.append(calc_errs(get_predict(prediction, t, b_back, n), get_actual(actual, t, b_back-n)))

    all_errs.append(errs)

  return all_errs

def calc_errs(predict_val, actual_val):
  return abs(predict_val-actual_val)/actual_val*1.

def get_predict(source, current, back, forward):
  return source[current+back][forward]

def get_actual(source, current, back):
  return source[current+back]


def test():

  weather_station = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
  accuweather = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
  ]

  print calc_confidence(accuweather, weather_station, 3, 5, 0)

test()