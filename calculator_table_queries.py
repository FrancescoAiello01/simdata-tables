import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp2d


def single_sheet_interpolation(table_data, runway_data, runway_length, aircraft_weight):
    """
        This function queries the table to find the best configuration given the table, aircraft weight and runway length
    """
    # find two closest
    closest_index = np.argsort(abs(runway_data - runway_length))
    closest_length_column = table_data[:, closest_index[0]]
    second_length_column = table_data[:, closest_index[1]]

    # interpolate two columns for given runway length
    interpolated_column_raw = interp2d(np.arange(0, 20), [runway_data[closest_index[0]], runway_data[closest_index[1]]],
                                       np.stack((closest_length_column, second_length_column)), kind='linear')
    interpolated_column = interpolated_column_raw(np.arange(0, 20), runway_length)

    # find two closest weight
    closest_weight_index = np.argsort(abs(interpolated_column - aircraft_weight))

    temp_index_1 = min(closest_weight_index[0], closest_weight_index[1])
    temp_index_2 = max(closest_weight_index[0],
                       closest_weight_index[1]) + 1  # Added +1 because python does not count the last number

    v1_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0] + 1]
    v1_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1] + 1]
    v1_interpolate_raw = interp2d(np.arange(0, 2), [runway_data[closest_index[0]], runway_data[closest_index[1]]],
                                  np.stack((v1_column_1, v1_column_2)), kind='linear')
    v1_interpolated = v1_interpolate_raw(np.arange(0, 2), runway_length)

    vr_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0] + 2]
    vr_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1] + 2]
    vr_interpolate_raw = interp2d(np.arange(0, 2), [runway_data[closest_index[0]], runway_data[closest_index[1]]],
                                  np.stack((vr_column_1, vr_column_2)), kind='linear')
    vr_interpolated = vr_interpolate_raw(np.arange(0, 2), runway_length)

    v2_column_1 = table_data[temp_index_1:temp_index_2, closest_index[0] + 3]
    v2_column_2 = table_data[temp_index_1:temp_index_2, closest_index[1] + 3]
    v2_interpolate_raw = interp2d(np.arange(0, 2), [runway_data[closest_index[0]], runway_data[closest_index[1]]],
                                  np.stack((v2_column_1, v2_column_2)), kind='linear')
    v2_interpolated = v2_interpolate_raw(np.arange(0, 2), runway_length)

    temp_column_1 = table_data[temp_index_1:temp_index_2, 0]
    temp_column_2 = table_data[temp_index_1:temp_index_2, 0]
    temp_interpolate_raw = interp2d(np.arange(0, 2), [runway_data[closest_index[0]], runway_data[closest_index[1]]],
                                    np.stack((temp_column_1, temp_column_2)), kind='linear')
    temp_interpolated = temp_interpolate_raw(np.arange(0, 2), runway_length)

    sheet1_result = np.array([temp_interpolated, v1_interpolated, vr_interpolated, v2_interpolated])

    weight1 = interpolated_column[temp_index_1]
    weight2 = interpolated_column[temp_index_2 - 1]  # Subtracting 1 because need to remove the +1 correction from above
    final_interpolate_raw = interp2d(np.arange(0, 4), [weight1, weight2],
                                     np.stack((sheet1_result[:, 0], sheet1_result[:, 1])), kind='linear')
    final_interpolated = final_interpolate_raw(np.arange(0, 4), aircraft_weight)
    final_interpolated = np.round(final_interpolated, decimals=0)

    return final_interpolated


def final_interpolation(table_data_1, runway_data_1, table_data_2, runway_data_2, runway_length, aircraft_weight,
                        pressure_altitude_raw, sheet1, sheet2):
    """
        This function gets the two best configurations (e.g. CONF1+F and CONF2) and interpolates the two
    """
    input_1 = single_sheet_interpolation(table_data_1, runway_data_1, runway_length, aircraft_weight)
    input_2 = single_sheet_interpolation(table_data_2, runway_data_2, runway_length, aircraft_weight)

    pressure_altitude_lower = int(str(sheet1) + "000")
    pressure_altitude_upper = int(str(sheet2) + "000")

    final_interpolate_raw = interp2d(np.arange(0, 4), [pressure_altitude_lower, pressure_altitude_upper],
                                     np.stack((input_1, input_2)), kind='linear')
    final_interpolated = final_interpolate_raw(np.arange(0, 4), pressure_altitude_raw)
    final_interpolated = np.round(final_interpolated, decimals=0)

    return final_interpolated


# sheet_extension = str(math.trunc(pressure_altitude))
# sheet_extension = sheet_extension + "000" + ".xlsx"

def find_best_config(air_pressure, runway_length, aircraft_weight):
    """
        This function preps the data and calls the helper functions to query it
    """
    first_table_row = 2
    max_table_row = 22
    pre = os.path.dirname(os.path.realpath(__file__))  # Our current running directory

    configs = {}

    def fill_configs(conf_number):
        # ---- CONFIG conf_number ----
        configs['config{}_0000_sheet'.format(conf_number)] = pd.ExcelFile(
            pre + '/{}0000.xlsx'.format(conf_number)).parse()
        configs['config{}_1000_sheet'.format(conf_number)] = pd.ExcelFile(
            pre + '/{}1000.xlsx'.format(conf_number)).parse()
        configs['config{}_2000_sheet'.format(conf_number)] = pd.ExcelFile(
            pre + '/{}2000.xlsx'.format(conf_number)).parse()
        # Prepare Data --> pressure altitude 0
        # TODO make changes from config1 to config{} .. .format(conf_number)
        configs['config{}_0000_sheet'.format(conf_number)] = configs['config{}_0000_sheet'.format(conf_number)].loc[
                                                             0:].fillna(0)
        configs['config{}_0000_complete'.format(conf_number)] = configs[
            'config{}_0000_sheet'.format(conf_number)].values
        configs['config{}_0000_data'.format(conf_number)] = configs['config{}_0000_complete'.format(conf_number)][
                                                            first_table_row:max_table_row, :]
        configs['config{}_0000_runway_data'.format(conf_number)] = configs[
                                                                       'config{}_0000_complete'.format(conf_number)][0,
                                                                   :]
        # Prepare Data --> pressure altitude 1000
        configs['config{}_1000_sheet'.format(conf_number)] = configs['config{}_1000_sheet'.format(conf_number)].loc[
                                                             0:].fillna(0)
        configs['config{}_1000_complete'.format(conf_number)] = configs[
            'config{}_1000_sheet'.format(conf_number)].values
        configs['config{}_1000_data'.format(conf_number)] = configs['config{}_1000_complete'.format(conf_number)][
                                                            first_table_row:max_table_row, :]
        configs['config{}_1000_runway_data'.format(conf_number)] = configs[
                                                                       'config{}_1000_complete'.format(conf_number)][0,
                                                                   :]
        # Prepare Data --> pressure altitude 2000
        configs['config{}_2000_sheet'.format(conf_number)] = configs['config{}_2000_sheet'.format(conf_number)].loc[
                                                             0:].fillna(0)
        configs['config{}_2000_complete'.format(conf_number)] = configs[
            'config{}_2000_sheet'.format(conf_number)].values
        configs['config{}_2000_data'.format(conf_number)] = configs['config{}_2000_complete'.format(conf_number)][
                                                            first_table_row:max_table_row, :]
        configs['config{}_2000_runway_data'.format(conf_number)] = configs[
                                                                       'config{}_2000_complete'.format(conf_number)][0,
                                                                   :]

    for i in range(1, 4):
        fill_configs(i)

    # Determine best pressure altitude for each configuration
    pressure_altitude_raw = (1 - (air_pressure / 1013.25) ** 0.190284) * 145366.45  # Formula for pressure altitude
    table_choices = np.array([0, 1000, 2000])
    pressure_altitude_indices = np.argsort(abs(table_choices - pressure_altitude_raw))
    sheet1 = pressure_altitude_indices[0]
    sheet2 = pressure_altitude_indices[1]

    # << ------------------------ Prepare Data ------------------------ >>
    # Configuration 1 full table data
    conf1_1 = configs['config1_' + str(sheet1) + '000_data']
    conf1_2 = configs['config1_' + str(sheet2) + '000_data']
    # Configuration 1 runway data
    conf1_rwy_1 = configs['config1_' + str(sheet1) + '000_runway_data']
    conf1_rwy_2 = configs['config1_' + str(sheet2) + '000_runway_data']
    # Find closest runway length
    conf1_rwy_length_index = np.argmin(abs(conf1_rwy_1 - runway_length))
    conf1_rwy_length_index_2 = np.argmin(abs(conf1_rwy_2 - runway_length))

    # Configuration 2 full table data
    conf2_1 = configs['config2_' + str(sheet1) + '000_data']
    conf2_2 = configs['config2_' + str(sheet2) + '000_data']
    # Configuration 2 runway data
    conf2_rwy_1 = configs['config2_' + str(sheet1) + '000_runway_data']
    conf2_rwy_2 = configs['config2_' + str(sheet2) + '000_runway_data']
    # Find closest runway length
    conf2_rwy_length_index = np.argmin(abs(conf2_rwy_1 - runway_length))
    conf2_rwy_length_index_2 = np.argmin(abs(conf2_rwy_2 - runway_length))

    # Configuration 2 full table data
    conf3_1 = configs['config3_' + str(sheet1) + '000_data']
    conf3_2 = configs['config3_' + str(sheet2) + '000_data']
    # Configuration 2 runway data
    conf3_rwy_1 = configs['config3_' + str(sheet1) + '000_runway_data']
    conf3_rwy_2 = configs['config3_' + str(sheet2) + '000_runway_data']
    # Find closest runway length
    conf3_rwy_length_index = np.argmin(abs(conf3_rwy_1 - runway_length))
    conf3_rwy_length_index_2 = np.argmin(abs(conf3_rwy_2 - runway_length))

    # ----------- Add final configuration to 2D array -----------
    # Config 1+F
    conf_final = np.zeros((4, 3))
    conf_final[:, 0] = final_interpolation(conf1_1, conf1_rwy_1, conf1_2, conf1_rwy_2, runway_length, aircraft_weight,
                                           pressure_altitude_raw, sheet1, sheet2)
    # Config 2
    conf_final[:, 1] = final_interpolation(conf2_1, conf2_rwy_1, conf2_2, conf2_rwy_2, runway_length, aircraft_weight,
                                           pressure_altitude_raw, sheet1, sheet2)
    # Config 3
    conf_final[:, 2] = final_interpolation(conf3_1, conf3_rwy_1, conf3_2, conf3_rwy_2, runway_length, aircraft_weight,
                                           pressure_altitude_raw, sheet1, sheet2)

    # Select best configuration
    best_configuration_index = np.argwhere(
        conf_final[0, :] == np.amax(conf_final[0, :]))  # Find maximum temperature index (can be multiple)
    best_configuration_sum = np.reshape(conf_final[:, best_configuration_index], (4, 2))  # Transpose
    best_configuration_index = np.argmin(np.sum(best_configuration_sum,
                                                0))  # If multiple temperatures, find the index of the configuration with minimium speed

    best_configuration = conf_final[:, best_configuration_index]
    best_configuration_name = "CONFIG " + str(best_configuration_index + 1)

    return [best_configuration_name, best_configuration]
