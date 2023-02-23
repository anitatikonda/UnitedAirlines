
# Parser Credit: @anitatikonda

## import statements
import pandas as pd
import numpy as np
from datetime import datetime

# import csv file and save as dataframe
data = pd.read_csv('Boarding Rate Observation.csv')

# make a local copy of dataframe before changes are made
boardrate_df = data.copy()

# filtered out Group 6 tests, eliminated 0 pax count rows, eliminated first 11 rows (before 2/15)
brate_filtered_df = boardrate_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) # brute forcing dropping of dates before 2/15
brate_filtered_df = brate_filtered_df[brate_filtered_df['Incentive'] == 'Group 6 test']
brate_filtered_df = brate_filtered_df[brate_filtered_df['Num_PAX'] > 0]

# filtered out pax_timestamps
pax_rate_time = brate_filtered_df['PAX_Timestamps']
# note that here, pax_rate_time is a series (single-row dataframe)

# list made for simplicity
pax_rate_time_list = []

# list parser; removes '-REMOVE' pax times from each entry
for index, values in pax_rate_time.items():
	temp_list = values.split(',')
	for j in temp_list:
		if 'REMOVE' in j:
			temp_list.remove(j)
	pax_rate_time_list.append(temp_list) # list of lists of pax timestamps

# declaration of new list
pax_time_master_list = []

# takes out 'AM' and 'PM' and creates list with hr:min (doesn't eliminate)
for item in pax_rate_time_list:
	list_holder = []
	count = 1
	for i in range(0, len(item)):
		inew = item[i][:-3]
		inew = inew.replace(' ', '') # replaces spaces with empty space
		list_holder.append(inew[:-3])
	pax_time_master_list.append(list_holder)

# new list declaration for timeline
pax_timeline_list = []


for item in pax_time_master_list:
	minute = 1
	count_list = []
	count = 1
	unique_timestring_list = []
	initial = item[0] # initializes first timestamp
	initialhr = initial[:2] # initializes first timestamp hr; : doesn't matter
	initialmin = int(initial[-2:]) # initializes first timestamp min
	save = (0, 0)

	for j in item:
		if not j in unique_timestring_list:
			if j[:2] == initialhr:
				minute = int(j[-2:]) - initialmin + 1 # + 1 is to adjust for graph
				if minute == 0:
					minute = 1
			else:
				minute = 60 - initialmin + int(j[-2:]) + 1 # works! :D
			count = 1 # should only be assigned 1 if datapoint, else 0
			unique_timestring_list.append(j)
			count_list.append((minute, count))

			save = (minute, count)

		else:
			# time to fix this! use save here
			count_list[count_list.index(save)] = (minute, count + 1)
			count += 1
			save = (minute, count)
	pax_timeline_list.append(count_list)

# initialization of dataframe list for all mins 01-45; empty declarations
pax_df_list = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]\
,[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]\
,[0],[0],[0],[0],[0]]

# construction of dataframe for analysis (first 45 min of pax boarding)
for flight in pax_timeline_list:
	for i in range(1, 46):
		value = 0
		for tuple_ in flight:
			if tuple_[0] == i:
				value = tuple_[1]
		pax_df_list[i - 1].append(value)

pax_timeline = pd.DataFrame(pax_df_list)
pax_timeline_t = pax_timeline.transpose()
pax_timeline_final = pax_timeline_t.drop(0)
print(pax_timeline_final)

# export to csv
pax_timeline_final.to_csv('PAX_Boarding_Rate_Timeline.csv')

