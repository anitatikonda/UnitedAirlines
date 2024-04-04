# parser credit: @anitatikonda
# passenger rate parser converter
# jet bridge to aircraft entry passenger flow measurement & (control v. pilot) analysis
# used for United Airlines WILMA Group 6 Testing at LAX

# import statements
import pandas as pd
import numpy as np
from datetime import datetime

# import data
data = pd.read_csv('Boarding Rate Observation (10).csv')
boardrate_df = data.copy() # local copy
print(len(boardrate_df.index))

# start and end date setting
start_date = '2/16/2023'
end_date = '3/21/2023'

# data filter function
def parser_filter(dropped_rows_count = 0, test_incentive = 'Group 6 test', pax_greater_than = 0, station = 'MSP'):
	num_list = []
	for i in range(0, dropped_rows_count):
		num_list.append(i)
	brate_filtered_df = boardrate_df.drop(num_list)
	print(len(brate_filtered_df.index))
	brate_filtered_df = brate_filtered_df[brate_filtered_df['Incentive'] == test_incentive]
	print(len(brate_filtered_df.index))
	brate_filtered_df = brate_filtered_df[brate_filtered_df['Station'] == station]
	print(len(brate_filtered_df.index))
	brate_filtered_df = brate_filtered_df[brate_filtered_df['Num_PAX'] > pax_greater_than]
	print(len(brate_filtered_df.index))
	return brate_filtered_df

brate_filtered_df = parser_filter(0, 'Control test', 0, 'LAX')
print(len(brate_filtered_df.index))

# returns pax timestamps from dataframe
pax_rate_time = brate_filtered_df['PAX_Timestamps']

# initialize lists
pax_rate_time_list = [] # deals with removing REMOVE's
pax_time_master_list = [] # deals with removing 'AM' and 'PM'
pax_timeline_list = [] # deals with the unordered pax timeline

# parses list and removes instances of '-REMOVE' in each flight entry
for index, values in pax_rate_time.items():
	temp_list = values.split(',')
	for j in temp_list:
		if 'REMOVE' in j:
			temp_list.remove(j)
	pax_rate_time_list.append(temp_list) # list of lists of pax timestamps

# takes out 'AM' and 'PM'
for item in pax_rate_time_list:
	list_holder = []
	count = 1
	for i in range(0, len(item)):
		inew = item[i][:-3] # takes out last three characters ' AM' or ' PM'
		inew = inew.replace(' ', '') # replaces spaces with empty space
		list_holder.append(inew[:])
	pax_time_master_list.append(list_holder)

# Mark IV parsing method
rate_list_by_flight = [] # will contain all data needed for rate-by-min for all flights

# parses through each flight's list of timestamps
for flights in pax_time_master_list:

	# initializations
	flight_rate = [] # builds rate-by-minute timeline for each flight
	data = (0, 0) 
	starting_index = 1

	initial_min = int(flights[0][-5:-3]) # takes first boarding min of first flight
	initial_sec = int(flights[0][-2:]) # takes first boarding sec of first flight

	for i in range(starting_index, 45): # boarding mins 1-45
		count = 0
		data = (i, 0) # if the boarding min DNE, gets filled with (minute, count = 0)
		if initial_min == 60:
			initial_min = 0
		for timestamp in flights:
			if int(timestamp[-5:-3]) == initial_min:
				if int(timestamp[-2:]) >= initial_sec: # if the min falls short of the current 'min tier'
					count += 1 # count it towards current min
					data = (i, count)
			elif int(timestamp[-5:-3]) - initial_min == 1:
				if int(timestamp[-2:]) < initial_sec: # if the min falls short the next 'min tier'
					count += 1 # count it towards current min
					data = (i, count)
		
		initial_min += 1 # keep unity between boarding minutes (recorded and 1-45)
		flight_rate.append(data)
	rate_list_by_flight.append(flight_rate) # adds to flight list

pax_timeline_list = rate_list_by_flight # becomes master flight list
# pax timestamps have been calculated at this point

# initialization of dataframe list for all mins 01-45
pax_df_list = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]\
,[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]\
,[0],[0],[0],[0],[0]]

# construction of dataframe for analysis (first 45 min of pax boarding is desired for analysis)
for flight in pax_timeline_list:
	for i in range(1, 46):
		value = 0
		for tuple_ in flight:
			if tuple_[0] == i:
				value = tuple_[1]
		pax_df_list[i - 1].append(value)

pax_timeline = pd.DataFrame(pax_df_list)
pax_timeline_t = pax_timeline.transpose() # switching of rows and columns
pax_timeline_final = pax_timeline_t.drop(0)
print(pax_timeline_final)

# export to csv
pax_timeline_final.to_csv('PAX_Scan_Rate_Timeline_LAX_Ctrl.csv')
