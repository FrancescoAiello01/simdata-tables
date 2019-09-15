import math
import pandas as pd
import numpy as np
from scipy.interpolate import interp2d

#Inputs
air_pressure = 990
runway_length_uncorrected = 2750
head_wind = 10
slope_percent = 1 # Percentage (uphill is positive, downhill is negative)
temperature = 30
aircraft_weight = 66

# Corrections for wind and runway slope
wind_slope_correction_table = np.array([
[1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500], # Runway length(m)
[6.5, 7, 8, 8.5, 9.5, 10, 11, 11.5, 12.5], # Effect of wind
[160, 215, 270, 325, 380, 435, 490, 545, 600], # Effect of runway slope uphill
[17, 23, 29, 36, 42, 48, 56, 61, 67] # Effect of runway slop downhill
])

closest_runway_length_index = np.argmin(abs(wind_slope_correction_table[0,:] - runway_length_uncorrected))
effect_of_wind = wind_slope_correction_table[1, closest_runway_length_index]
# Runway slope
if (slope_percent >= 0):
    effect_of_runway_slope = wind_slope_correction_table[2, closest_runway_length_index] * slope_percent
elif (slope_percent < 0):
    effect_of_runway_slope = wind_slope_correction_table[3, closest_runway_length_index] * abs(slope_percent)
else:
    print("Unable to determine runway slope correction")

runway_length = runway_length_uncorrected + (effect_of_wind * head_wind) - effect_of_runway_slope

# sheet_extension = str(math.trunc(pressure_altitude))
# sheet_extension = sheet_extension + "000" + ".xlsx"

first_table_row = 2
max_table_row = 22

# ---- CONFIG 1 ----
config1_0000_sheet = pd.ExcelFile('10000.xlsx').parse()
config1_1000_sheet = pd.ExcelFile('11000.xlsx').parse()
config1_2000_sheet = pd.ExcelFile('12000.xlsx').parse()
# Prepare Data --> pressure altitude 0
config1_0000_sheet = config1_0000_sheet.loc[0:].fillna(0)
config1_0000_complete = config1_0000_sheet.values
config1_0000_data = config1_0000_complete[first_table_row:max_table_row,:]
config1_0000_runway_data = config1_0000_complete[0,:]
# Prepare Data --> pressure altitude 1000
config1_1000_sheet = config1_1000_sheet.loc[0:].fillna(0)
config1_1000_complete = config1_1000_sheet.values
config1_1000_data = config1_1000_complete[first_table_row:max_table_row,:]
config1_1000_runway_data = config1_1000_complete[0,:]
# Prepare Data --> pressure altitude 2000
config1_2000_sheet = config1_2000_sheet.loc[0:].fillna(0)
config1_2000_complete = config1_2000_sheet.values
config1_2000_data = config1_2000_complete[first_table_row:max_table_row,:]
config1_2000_runway_data = config1_2000_complete[0,:]

# ---- CONFIG 2 ----
config2_0000_sheet = pd.ExcelFile('20000.xlsx').parse()
config2_1000_sheet = pd.ExcelFile('21000.xlsx').parse()
config2_2000_sheet = pd.ExcelFile('22000.xlsx').parse()
# Prepare Data --> pressure altitude 0
config2_0000_sheet = config2_0000_sheet.loc[0:].fillna(0)
config2_0000_complete = config2_0000_sheet.values
config2_0000_data = config2_0000_complete[first_table_row:max_table_row,:]
config2_0000_runway_data = config2_0000_complete[0,:]
# Prepare Data --> pressure altitude 1000
config2_1000_sheet = config2_1000_sheet.loc[0:].fillna(0)
config2_1000_complete = config2_1000_sheet.values
config2_1000_data = config2_1000_complete[first_table_row:max_table_row,:]
config2_1000_runway_data = config2_1000_complete[0,:]
# Prepare Data --> pressure altitude 2000
config2_2000_sheet = config2_2000_sheet.loc[0:].fillna(0)
config2_2000_complete = config2_2000_sheet.values
config2_2000_data = config2_2000_complete[first_table_row:max_table_row,:]
config2_2000_runway_data = config2_2000_complete[0,:]

# ---- CONFIG 3 ----
config3_0000_sheet = pd.ExcelFile('30000.xlsx').parse()
config3_1000_sheet = pd.ExcelFile('31000.xlsx').parse()
config3_2000_sheet = pd.ExcelFile('32000.xlsx').parse()
# Prepare Data --> pressure altitude 0
config3_0000_sheet = config3_0000_sheet.loc[0:].fillna(0)
config3_0000_complete = config3_0000_sheet.values
config3_0000_data = config3_0000_complete[first_table_row:max_table_row,:]
config3_0000_runway_data = config3_0000_complete[0,:]
# Prepare Data --> pressure altitude 1000
config3_1000_sheet = config3_1000_sheet.loc[0:].fillna(0)
config3_1000_complete = config3_1000_sheet.values
config3_1000_data = config3_1000_complete[first_table_row:max_table_row,:]
config3_1000_runway_data = config3_1000_complete[0,:]
# Prepare Data --> pressure altitude 2000
config3_2000_sheet = config3_2000_sheet.loc[0:].fillna(0)
config3_2000_complete = config3_2000_sheet.values
config3_2000_data = config3_2000_complete[first_table_row:max_table_row,:]
config3_2000_runway_data = config3_2000_complete[0,:]

# Determine best pressure altitude for each configuration
pressure_altitude_raw = (1-(air_pressure/1013.25)**0.190284)*145366.45 # Formula for pressure altitude
table_choices = np.array([0, 1000, 2000])
pressure_altitude_indices = np.argsort(abs(table_choices - pressure_altitude_raw))
sheet1 = pressure_altitude_indices[0]
sheet2 = pressure_altitude_indices[1]
print(sheet1, sheet2)


# << ------------------------ Prepare Data ------------------------ >>
# Configuration 1 full table data
conf1_1 = globals()['config1_' + str(sheet1) + '000_data']
conf1_2 = globals()['config1_' + str(sheet2) + '000_data']
# Configuration 1 runway data
conf1_rwy_1 = globals()['config1_' + str(sheet1) + '000_runway_data']
conf1_rwy_2 = globals()['config1_' + str(sheet2) + '000_runway_data']
# Find closest runway length
conf1_rwy_length_index = np.argmin(abs(conf1_rwy_1 - runway_length))
conf1_rwy_length_index_2 = np.argmin(abs(conf1_rwy_2 - runway_length))


# Configuration 2 full table data
conf2_1 = globals()['config2_' + str(sheet1) + '000_data']
conf2_2 = globals()['config2_' + str(sheet2) + '000_data']
# Configuration 2 runway data
conf2_rwy_1 = globals()['config2_' + str(sheet1) + '000_runway_data']
conf2_rwy_2 = globals()['config2_' + str(sheet2) + '000_runway_data']
# Find closest runway length
conf2_rwy_length_index = np.argmin(abs(conf2_rwy_1 - runway_length))
conf2_rwy_length_index_2 = np.argmin(abs(conf2_rwy_2 - runway_length))


# Configuration 2 full table data
conf3_1 = globals()['config3_' + str(sheet1) + '000_data']
conf3_2 = globals()['config3_' + str(sheet2) + '000_data']
# Configuration 2 runway data
conf3_rwy_1 = globals()['config3_' + str(sheet1) + '000_runway_data']
conf3_rwy_2 = globals()['config3_' + str(sheet2) + '000_runway_data']
# Find closest runway length
conf3_rwy_length_index = np.argmin(abs(conf3_rwy_1 - runway_length))
conf3_rwy_length_index_2 = np.argmin(abs(conf3_rwy_2 - runway_length))


def single_sheet_interpolation(table_data, runway_data):
    # find two closest
    closest_index = np.argsort(abs(runway_data - runway_length))
    closest_length_column = table_data[:, closest_index[0]]
    second_length_column = table_data[:, closest_index[1]]

    # interpolate two columns for given runway length
    interpolated_column_raw = interp2d(np.arange(0,20), [runway_data[closest_index[0]], runway_data[closest_index[1]]], np.stack((closest_length_column, second_length_column)), kind='linear')
    interpolated_column = interpolated_column_raw(np.arange(0, 20), runway_length)

    # find two closest weight
    closest_weight_index = np.argsort(abs(interpolated_column - aircraft_weight))
    closest_weight = interpolated_column[closest_weight_index[0]]
    second_weight = interpolated_column[closest_weight_index[1]]

    temp_index_1 = min(closest_weight_index[0], closest_weight_index[1])
    temp_index_2 = max(closest_weight_index[0], closest_weight_index[1])+1 # Added +1 because python does not count the last number

    v1_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0]+1]
    v1_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1]+1]
    v1_interpolate_raw = interp2d(np.arange(0,2), [runway_data[closest_index[0]], runway_data[closest_index[1]]], np.stack((v1_column_1, v1_column_2)), kind='linear')
    v1_interpolated = v1_interpolate_raw(np.arange(0, 2), runway_length)

    vr_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0]+2]
    vr_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1]+2]
    vr_interpolate_raw = interp2d(np.arange(0,2), [runway_data[closest_index[0]], runway_data[closest_index[1]]], np.stack((vr_column_1, vr_column_2)), kind='linear')
    vr_interpolated = vr_interpolate_raw(np.arange(0, 2), runway_length)

    v2_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0]+3]
    v2_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1]+3]
    v2_interpolate_raw = interp2d(np.arange(0,2), [runway_data[closest_index[0]], runway_data[closest_index[1]]], np.stack((v2_column_1, v2_column_2)), kind='linear')
    v2_interpolated = v2_interpolate_raw(np.arange(0, 2), runway_length)

    temp_column_1 = table_data[temp_index_1:temp_index_2, 0]
    temp_column_2 = table_data[temp_index_1:temp_index_2, 0]
    temp_interpolate_raw = interp2d(np.arange(0,2), [runway_data[closest_index[0]], runway_data[closest_index[1]]], np.stack((temp_column_1, temp_column_2)), kind='linear')
    temp_interpolated = temp_interpolate_raw(np.arange(0, 2), runway_length)

    sheet1_result = np.array([temp_interpolated, v1_interpolated, vr_interpolated, v2_interpolated])


    weight1 = interpolated_column[temp_index_1]
    weight2 = interpolated_column[temp_index_2-1] # Subtracting 1 because need to remove the +1 correction from above
    final_interpolate_raw = interp2d(np.arange(0,4), [weight1, weight2], np.stack((sheet1_result[:,0], sheet1_result[:,1])), kind='linear')
    final_interpolated = final_interpolate_raw(np.arange(0, 4), aircraft_weight)
    final_interpolated = np.round(final_interpolated, decimals=0)

    return final_interpolated



def final_interpolation(table_data_1, runway_data_1, table_data_2, runway_data_2):
    input_1 = single_sheet_interpolation(table_data_1, runway_data_1)
    input_2 = single_sheet_interpolation(table_data_2, runway_data_2)

    pressure_altitude_lower = int(str(sheet1) + "000")
    pressure_altitude_upper = int(str(sheet2) + "000")

    final_interpolate_raw = interp2d(np.arange(0,4), [pressure_altitude_lower, pressure_altitude_upper], np.stack((input_1, input_2)), kind='linear')
    final_interpolated = final_interpolate_raw(np.arange(0, 4), pressure_altitude_raw)
    final_interpolated = np.round(final_interpolated, decimals=0)

    return final_interpolated

# Config 1+F
print(final_interpolation(conf1_1, conf1_rwy_1, conf1_2, conf1_rwy_2))
# Config 2
print(final_interpolation(conf2_1, conf2_rwy_1, conf2_2, conf2_rwy_2))
# Config 3
print(final_interpolation(conf3_1, conf3_rwy_1, conf3_2, conf3_rwy_2))
