import numpy as np
import pandas as pd

# Tables for minimum V2 speed
table_pressure_altitudes = [-1000, 0, 2000, 3000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000,
                            14000]
table_aircraft_weights = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

conf1 = pd.DataFrame(np.array([
    [123, 123, 123, 123, 123, 128, 133, 137, 142, 147],
    [123, 123, 123, 123, 123, 128, 133, 138, 142, 147],
    [121, 121, 121, 121, 122, 128, 133, 138, 143, 148],
    [120, 120, 120, 120, 122, 128, 133, 138, 143, 148],
    [119, 119, 119, 119, 123, 128, 133, 138, 143, 148],
    [118, 118, 118, 118, 123, 128, 133, 138, 143, 148],
    [117, 117, 117, 117, 123, 128, 133, 138, 144, 148],
    [116, 116, 116, 117, 123, 128, 133, 138, 143, 148],
    [115, 115, 115, 117, 123, 128, 133, 139, 143, 149],
    [113, 113, 113, 117, 123, 128, 134, 139, 144, 149],
    [112, 112, 112, 117, 123, 128, 134, 139, 144, 149],
    [111, 111, 111, 117, 123, 129, 134, 139, 144, 149],
    [109, 109, 111, 117, 123, 129, 134, 139, 144, 150],
    [108, 108, 111, 117, 123, 129, 134, 139, 144, 150],
    [106, 106, 111, 118, 124, 129, 134, 140, 145, 150],
    [104, 104, 111, 118, 124, 129, 134, 140, 145, 150],
]), index=table_pressure_altitudes,  # Pressure altitude is first column
    columns=table_aircraft_weights)  # Columns = takeoff weight (in 1000 of kg)

conf2 = pd.DataFrame(np.array([
    [123, 123, 123, 123, 123, 123, 126, 131, 136, 140],
    [122, 122, 122, 122, 122, 122, 126, 131, 136, 141],
    [121, 121, 121, 121, 121, 122, 126, 131, 136, 141],
    [120, 120, 120, 120, 120, 122, 127, 131, 136, 141],
    [119, 119, 119, 119, 119, 122, 127, 131, 136, 141],
    [118, 118, 118, 118, 118, 122, 127, 132, 136, 141],
    [117, 117, 117, 117, 117, 122, 127, 132, 136, 141],
    [115, 115, 115, 115, 117, 122, 127, 132, 137, 141],
    [114, 114, 114, 114, 117, 122, 127, 132, 137, 142],
    [113, 113, 113, 113, 117, 122, 127, 132, 137, 142],
    [112, 112, 112, 112, 117, 122, 127, 132, 137, 142],
    [110, 110, 110, 112, 117, 123, 127, 132, 137, 142],
    [109, 109, 109, 112, 118, 123, 127, 133, 137, 142],
    [108, 108, 108, 112, 118, 123, 128, 133, 137, 142],
    [106, 106, 106, 112, 118, 123, 128, 133, 138, 143],
    [104, 104, 106, 112, 118, 123, 128, 133, 138, 143],
]), index=table_pressure_altitudes,  # Pressure altitude is first column
    columns=table_aircraft_weights)  # Columns = takeoff weight (in 1000 of kg)

conf3 = pd.DataFrame(np.array([
    [123, 123, 123, 123, 123, 123, 123, 128, 132, 137],
    [122, 122, 122, 122, 122, 122, 123, 128, 132, 137],
    [121, 121, 121, 121, 121, 121, 124, 128, 132, 137],
    [120, 120, 120, 120, 120, 120, 124, 128, 132, 137],
    [119, 119, 119, 119, 119, 119, 124, 128, 133, 137],
    [118, 118, 118, 118, 118, 119, 124, 128, 133, 138],
    [117, 117, 117, 117, 117, 119, 124, 129, 133, 138],
    [116, 116, 116, 116, 116, 119, 124, 129, 133, 138],
    [115, 115, 115, 115, 115, 120, 124, 129, 133, 138],
    [113, 113, 113, 113, 115, 120, 124, 129, 133, 138],
    [112, 112, 112, 112, 115, 120, 124, 129, 134, 138],
    [111, 111, 111, 111, 115, 120, 124, 129, 134, 138],
    [109, 109, 109, 110, 115, 120, 125, 129, 134, 139],
    [108, 108, 108, 110, 115, 120, 125, 129, 134, 139],
    [106, 106, 106, 110, 115, 120, 125, 130, 134, 139],
    [105, 105, 105, 110, 115, 120, 125, 130, 134, 139],
]), index=table_pressure_altitudes,  # Pressure altitude is first column
    columns=table_aircraft_weights)  # Columns = takeoff weight (in 1000 of kg)


def v2_speed_check_is_ok(v2speed, pressure_altitude, takeoff_weight, configuration):
    rounded_pressure_altitude = min(table_pressure_altitudes,
                                    key=lambda x: abs(x - pressure_altitude))  # Gets closest value in list
    rounded_takeoff_weight = min(table_aircraft_weights,
                                 key=lambda x: abs(x - takeoff_weight))  # Gets closest value in list
    if configuration == "CONF 1":
        v2_min_speed = conf1.loc[rounded_pressure_altitude, rounded_takeoff_weight]  # Query table
    elif configuration == "CONF 2":
        v2_min_speed = conf2.loc[rounded_pressure_altitude, rounded_takeoff_weight]  # Query table
    else:
        v2_min_speed = conf3.loc[rounded_pressure_altitude, rounded_takeoff_weight]  # Query table

    if v2speed < v2_min_speed:
        return False # Return False if our speed is less than the minimum speed
    return True

