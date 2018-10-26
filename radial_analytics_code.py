import csv
import pandas as p

#open and read
file = open('Hospital General Information.csv')
csv_file = p.read_csv(file, sep = ",", error_bad_lines=False)

#group  by state and county and count number of hospitals
df_by_state_county = csv_file.groupby(by=['State', 'County Name'])
count = df_by_state_county.size()

#reset rating type
csv_file.loc[(csv_file['Hospital overall rating'] == 'Not Available')] = 0
csv_file['Hospital overall rating'] = csv_file['Hospital overall rating'].astype("int")

#count hospital type
csv_file.reset_index()
filtered = csv_file.loc[csv_file['Hospital Type'] == 'Acute Care Hospitals']
state_county_filtered = filtered.groupby(by=['State', 'County Name'])
type_count = state_county_filtered.size()

#find average rating
rating = state_county_filtered['Hospital overall rating'].mean()

#merge created dataframes
result1 = p.merge(count.reset_index(), type_count.reset_index(), on=['State', 'County Name'])
result = p.merge(result1, rating.reset_index())
print(result)

#create csv
result.to_csv('out.csv', sep=',', header=['State', 'County', 'num_hospitals', 'num_acute_care_hospitals', 'avg_acute_care_rating'])

file.close()

