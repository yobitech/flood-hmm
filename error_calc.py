
import numpy as np
import pandas as pd

######################################
# 
# get_errors
# 
# gets the errors for sources of data compared to actual
# 
# Parameters
# -------
# actual : dataframe
#   columns 
# 
# Returns
# -------
# merged_df : dataframe
#   dataframe with all data sources merged together by time
# avg_errors_df : dataframe
#   dataframe with each column as a given measurement
#   and each row as a distinct source
# 
######################################

# get the errors for each source of data vs. the actual
def get_errors(actual, sources, measurements):

  count = 1
  avg_errs = {}

  # combining all of the data frames
  for source in sources:

    if count == 1:
      merged_df = actual.merge(source, 
        on='last_update', how='left', suffixes = ['', '_1'])
    else:
      merged_df = merged_df.merge(source, 
        on='last_update', how='left', suffixes = ['', '_'+str(count)])

    count += 1

  # find the differences and errors
  for measurement in measurements:

    avgs = []

    for i in range(1,len(sources)+1):

      merged_df[measurement+'_diff_'+str(i)] = merged_df[measurement] - merged_df[measurement+'_'+str(i)]
      merged_df[measurement+'_error_'+str(i)] = merged_df[measurement + '_diff_' + str(i)] / merged_df[measurement]

      mean = merged_df[measurement+'_error_'+str(i)].mean()
      avgs.append(mean)

    avg_errs[measurement] = avgs

  avg_errs_df = pd.DataFrame(avg_errs)

  return [merged_df, avg_errs_df]

# test the function
def test():

  weather_station = pd.DataFrame.from_csv('weather_station.csv')
  source1 = pd.DataFrame.from_csv('source1.csv')

  measurements = ['air_temp1', 'air_temp2', 'humdity', 'wind_speed', 'air_pressure', 'solar_radiation']

  print get_errors(weather_station, [source1, source1], measurements)

test()