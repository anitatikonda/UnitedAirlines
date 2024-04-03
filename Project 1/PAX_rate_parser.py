
# Parser Credit: @anitatikonda

# Instructions:
# The purpose of this parser is to extract recorded pax time stamps
# that mark when a passenger has boarded the aircarft from the jet
# bridge under the Group 6 boarding incentive (tested in Orange County
# and San Jose). This parser prepares a table that showcases each flight's
# passenger board rate per minute for 45 minutes of boarding entry.

## initializations (imports and local copy)
import pandas as pd
import numpy as np
from datetime import datetime

data = pd.read_csv('Boarding Rate Observation.csv')
boardrate_df = data.copy() # local copy

# --------------------------------------------------
# function for parser filters
# filters desired: Group 6 incentive, 2/15/23 onwards data, high pax counts
# these will all be implemented through function parameters

def parser_filter(dropped_rows_count = 11, test_incentive = 'Group 6 test', pax_greater_than = 0):
	num_list = []
	for i in range(0, dropped_rows_count):
		num_list.append(i)
	brate_filtered_df = boardrate_df.drop(num_list)
	brate_filtered_df = brate_filtered_df[brate_filtered_df['Incentive'] == test_incentive]
	brate_filtered_df = brate_filtered_df[brate_filtered_df['Num_PAX'] > pax_greater_than]
	return brate_filtered_df

# call to function
brate_filtered_df = parser_filter()

# --------------------------------------------------

# filtered out pax_timestamps
pax_rate_time = brate_filtered_df['PAX_Timestamps']

# lists
pax_rate_time_list = [] # to deal with 'REMOVE's
pax_time_master_list = [] # takes out 'AM' and 'PM'
pax_timeline_list = [] # builds the pax timeline (unordered)

# list parser; removes '-REMOVE' pax times from each entry
for index, values in pax_rate_time.items():
	temp_list = values.split(',')
	for j in temp_list:
		if 'REMOVE' in j:
			temp_list.remove(j)
	pax_rate_time_list.append(temp_list) # list of lists of pax timestamps


# takes out 'AM' and 'PM' and creates list with hr:min (doesn't eliminate)
for item in pax_rate_time_list:
	list_holder = []
	count = 1
	for i in range(0, len(item)):
		inew = item[i][:-3] # takes out last three characters ' AM' or ' PM'
		inew = inew.replace(' ', '') # replaces spaces with empty space
		list_holder.append(inew[:-3])
	pax_time_master_list.append(list_holder)


# this for-loop displays every pax-timestamp as min1, min2, etc.
for item in pax_time_master_list:
	minute = 1
	count_list = []
	count = 1
	unique_timestring_list = []
	initial = item[0] # initializes first timestamp
	initialhr = initial[:2] # initializes first timestamp hr; : doesn't matter
	initialmin = int(initial[-2:]) # initializes first timestamp min
	save = (0, 0)

	# after the above initializations, there are 2 cases we concern
	# Case 1: our minute already exists in our table (so we update count)
	# Case 2: our minute does not exist in our table (so we initialize new one)

	for j in item: # for every flight
		if not j in unique_timestring_list: # Case 1
			if j[:2] == initialhr:
				minute = int(j[-2:]) - initialmin + 1 # +1 adjusts for graph
				if minute == 0:
					minute = 1
			else:
				minute = 60 - initialmin + int(j[-2:]) + 1
			count = 1 # should only be assigned 1 if datapoint, else 0
			unique_timestring_list.append(j)
			count_list.append((minute, count))

			save = (minute, count) # save is the new 'updated' or added minute

		else: # Case 2
			count_list[count_list.index(save)] = (minute, count + 1)
			count += 1
			save = (minute, count)
	pax_timeline_list.append(count_list)

# --------------------------------------------------

# rest of below is data manipulation, pax timestamps have been calculated at this point

# initialization of dataframe list for all mins 01-45; empty declarations help
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
pax_timeline_t = pax_timeline.transpose() # switching of rows and columns
pax_timeline_final = pax_timeline_t.drop(0)
print(pax_timeline_final)

# export to csv
pax_timeline_final.to_csv('PAX_Boarding_Rate_Timeline.csv')

# --------------------------------------------------

# archives
# if the function method does not work, replace lines 29-36 with
# the code between ''' below

'''
# here are the filters for our tests
# - only want Group 6 incentives
# - take out rows with 0 pax counts (can adjust for higher numbers, e.g. 10)
# - eliminated first 11 rows that contained pre 2/15/23 data
brate_filtered_df = boardrate_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) # brute-force dropping method
brate_filtered_df = brate_filtered_df[brate_filtered_df['Incentive'] == 'Group 6 test']
brate_filtered_df = brate_filtered_df[brate_filtered_df['Num_PAX'] > 0]
'''
