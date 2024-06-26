# -*- coding: utf-8 -*-



import pandas as pd

import pandas as pd

df_damages=pd.read_csv("/content/sample_data/CSV/Damages.csv")
df_charges=pd.read_csv("/content/sample_data/CSV/Charges.csv")
df_data_dictionary=pd.read_excel("/content/sample_data/CSV/Data Dictionary.xlsx")
df_endorse=pd.read_csv("/content/sample_data/CSV/Endorse.csv")
df_primary_person = pd.read_csv("/content/sample_data/CSV/Primary_Person.csv")
df_restrict=pd.read_csv("/content/sample_data/CSV/Restrict.csv")
df_units=pd.read_csv("/content/sample_data/CSV/Units.csv")

print("df_damages:",df_damages.columns)
print("df_charges:",df_charges.columns)
print("df_data_dictionary:",df_data_dictionary.columns)
print("df_endorse:",df_endorse.columns)
print("df_primary_person:",df_primary_person.columns)
print("df_restrict:",df_restrict.columns)
print("df_units:",df_units.columns)

male_fatalities = df_primary_person[(df_primary_person['PRSN_GNDR_ID'] == 'Male') & (df_primary_person['DEATH_CNT'] > 0)]['CRASH_ID'].nunique()
print("Number of crashes with male fatalities:", male_fatalities)

two_wheelers = df_primary_person[df_primary_person['PRSN_HELMET_ID'] != 'NOT APPLICABLE']['CRASH_ID'].nunique()
print("Number of two-wheelers booked for crashes:", two_wheelers)

female_involved = df_primary_person[df_primary_person['PRSN_GNDR_ID'] == 'FEMALE']
state_with_most_female_involved = female_involved['DRVR_LIC_STATE_ID'].value_counts().idxmax()
print("State with highest number of female-involved accidents:", state_with_most_female_involved)

injuries = df_units.groupby('VEH_MAKE_ID')['TOT_INJRY_CNT'].sum().sort_values(ascending=False)
top_5_to_15_veh_make_ids = injuries.iloc[4:15]
print("Top 5th to 15th VEH_MAKE_IDs contributing to largest number of injuries including deaths:", top_5_to_15_veh_make_ids)

alcohol_crashes = df_primary_person[df_primary_person['PRSN_ALC_RSLT_ID'].notnull()]
top_5_zip_codes = alcohol_crashes['DRVR_ZIP'].value_counts().head(5)
print("Top 5 Zip Codes with highest number of alcohol-involved crashes:", top_5_zip_codes)

# Damage flag which depicts damage level above 4
damage_flag = ['DAMAGED 5', 'DAMAGED 6', 'DAMAGED 7 HIGHEST']

# Filter df_units for vehicles with damage level above 4
filtered_units = df_units[(df_units['VEH_DMAG_SCL_1_ID'].isin(damage_flag)) | (df_units['VEH_DMAG_SCL_2_ID'].isin(damage_flag))]

# Merge filtered df_units with df_damages on 'CRASH_ID'
damages_units_join_df = pd.merge(filtered_units, df_damages, on='CRASH_ID', how='inner')

# Identify distinct values of DAMAGED_PROPERTY which include 'NO DAMAGE'
distinct_damaged_property = damages_units_join_df['DAMAGED_PROPERTY'].unique()
no_damage_property_flag = [prop for prop in distinct_damaged_property if 'NO DAMAGE' in prop.upper()]

# Define car types
car_types = ['PASSENGER CAR, 2-DOOR', 'PASSENGER CAR, 4-DOOR', 'POLICE CAR/TRUCK', 'SPORT UTILITY VEHICLE', 'NEV-NEIGHBORHOOD ELECTRIC VEHICLE', 'VAN']

# Define non-insurance flag
non_insurance_flag = ['NA']

# Filter for vehicles which have insurance and are of car type, and did not damage property
filtered_df = damages_units_join_df[
    (~damages_units_join_df['FIN_RESP_TYPE_ID'].isin(non_insurance_flag)) &
    (damages_units_join_df['VEH_BODY_STYL_ID'].isin(car_types)) &
    (damages_units_join_df['DAMAGED_PROPERTY'].isin(no_damage_property_flag))
]

# Count distinct CRASH_IDs
distinct_crash_ids_count = filtered_df['CRASH_ID'].nunique()

print("Count of Distinct Crash IDs where No Damaged Property was observed and Damage Level is above 4 and car avails Insurance:", distinct_crash_ids_count)

# Extract distinct speeding-related charges
speeding_flag = df_charges[df_charges['CHARGE'].str.upper().str.contains('SPEED')]['CHARGE'].unique()

# Filter data for car types
car_types = ['PASSENGER CAR, 2-DOOR', 'PASSENGER CAR, 4-DOOR', 'POLICE CAR/TRUCK', 'SPORT UTILITY VEHICLE', 'NEV-NEIGHBORHOOD ELECTRIC VEHICLE', 'VAN']
filtered_units = df_units[df_units['VEH_BODY_STYL_ID'].isin(car_types)]

# DRIVER LICENSE TYPE
license_type_id = ['COMMERCIAL DRIVER LIC.', 'OCCUPATIONAL', 'DRIVER LICENSE']

# Merge primary_person_df with filtered_units
person_units_join_df = pd.merge(df_primary_person, filtered_units, on=['CRASH_ID', 'UNIT_NBR'], how='outer')

# Identify the top 25 states with the highest number of car crashes
states_highest_car_crash = person_units_join_df['VEH_LIC_STATE_ID'].value_counts().nlargest(25).index.tolist()

# Identify the top 10 used vehicle colors
top_vehicle_colors = person_units_join_df[person_units_join_df['VEH_COLOR_ID'] != 'NA']['VEH_COLOR_ID'].value_counts().nlargest(10).index.tolist()

# Combine all filters and find the top 5 vehicle makes involved in speeding-related offenses
filtered_df = person_units_join_df[
    (person_units_join_df['VEH_COLOR_ID'].isin(top_vehicle_colors)) &
    (person_units_join_df['VEH_LIC_STATE_ID'].isin(states_highest_car_crash)) &
    (person_units_join_df['DRVR_LIC_TYPE_ID'].isin(license_type_id))
]

# Join with charges data to filter for speeding-related offenses
result_df = pd.merge(filtered_df, df_charges[df_charges['CHARGE'].isin(speeding_flag)], on=['CRASH_ID', 'UNIT_NBR'])

# Group by vehicle make and get the top 5
top_5_vehicle_makes = result_df['VEH_MAKE_ID'].value_counts().nlargest(5).index.tolist()

print('Top 5 Vehicle Makes where drivers are charged with speeding related offences, has licensed Drivers, uses top 10 used vehicle colours and has car licensed with the Top 25 states with highest number of offences:')
print(top_5_vehicle_makes)

results = {
    "Analysis 1": male_fatalities,
    "Analysis 2": two_wheelers,
    "Analysis 3": state_with_most_female_involved,
    "Analysis 4": top_5_to_15_veh_make_ids.to_dict(),
    "Analysis 5": top_5_zip_codes.to_dict(),
    "Analysis 6": distinct_crash_ids_count,
    "Analysis 7": top_5_vehicle_makes
}

results_df = pd.DataFrame(list(results.items()), columns=['Analysis', 'Result'])
results_df.to_csv('/content/sample_data/CSV/crash_analysis_results.csv', index=False)
