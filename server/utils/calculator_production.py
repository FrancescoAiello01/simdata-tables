import argparse
import sys
import numpy as np
from .calculator_table_queries import find_best_config
from .calculator_min_v2_check import v2_speed_check_is_ok

# Test input: --air_pressure 990 --airport_elevation 1000 --outside_air_temp 35 --runway_length_uncorrected 2750 --head_wind 10 --slope_percent 1 --aircraft_weight 66 --AP_registration False --air_conditioning False --engine_anti_ice True --total_anti_ice False --operational_CG_percentage 26

def correct_runway_length(runway_length_uncorrected, slope_percent, head_wind):
    # Corrections for wind and runway slope
    wind_slope_correction_table = np.array([
        [1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500],  # Runway length(m)
        [6.5, 7, 8, 8.5, 9.5, 10, 11, 11.5, 12.5],  # Effect of wind
        [160, 215, 270, 325, 380, 435, 490, 545, 600],  # Effect of runway slope uphill
        [17, 23, 29, 36, 42, 48, 56, 61, 67]  # Effect of runway slope downhill
    ])

    closest_runway_length_index = np.argmin(abs(wind_slope_correction_table[0, :] - runway_length_uncorrected))
    effect_of_wind = wind_slope_correction_table[1, closest_runway_length_index]
    # Runway slope
    if slope_percent >= 0:
        effect_of_runway_slope = wind_slope_correction_table[2, closest_runway_length_index] * slope_percent
    elif slope_percent < 0:
        effect_of_runway_slope = wind_slope_correction_table[3, closest_runway_length_index] * abs(slope_percent)

    runway_length = runway_length_uncorrected + (effect_of_wind * head_wind) - effect_of_runway_slope
    return runway_length


def ac_adjustment(air_conditioning, AP_registration):
    if air_conditioning == "True":
        temp_ac = 0
    else:
        if AP_registration == "True" and air_conditioning == "False":
            temp_ac = 5
        else:
            temp_ac = 7
    return temp_ac


def engine_adjustment(engine_anti_ice):
    if engine_anti_ice == "False":
        temp_engine_ai = 0
    else:
        temp_engine_ai = -5
    return temp_engine_ai


def total_anti_ice_adjustment(total_anti_ice):
    if total_anti_ice == "False":
        total_anti_ice_modifier = 0
    else:
        total_anti_ice_modifier = -11
    return total_anti_ice_modifier


def calculate_tmax_flex(AP_registration, airport_elevation):
    if AP_registration == "True":
        tmax_flex = 15 - airport_elevation / 1000 * 2 + 70
    else:
        tmax_flex = 15 - airport_elevation / 1000 * 2 + 53
    return tmax_flex


def flex_temp_adjustment(temp_engine_ai, total_anti_ice_modifier, best_config, temp_ac):
    if temp_engine_ai < 0 and total_anti_ice_modifier < 0:
        flex_temp = best_config[0] + temp_ac + total_anti_ice_modifier
    else:
        flex_temp = best_config[0] + temp_ac + temp_engine_ai + total_anti_ice_modifier
    return flex_temp


# Note: TREF is not used here because it varies by location. This is just an inaccuracy we have to accept.
# Original if statement looked like this:
# if ((flex_temp < outside_air_temp + 1 or flex_temp < TREF + 1) and flex_temp > tmax_flex):
def flex_test(flex_temp, outside_air_temp):
    if flex_temp < outside_air_temp + 1:
        flex_possible = False
    else:
        flex_possible = True
    return flex_possible


def D_QNH(air_pressure):
    t_flex_adjustment_factor = -2
    if air_pressure > 1013:
        result = (air_pressure - 1013) / 10 * t_flex_adjustment_factor
    else:
        result = (1013 - air_pressure) / 10 * t_flex_adjustment_factor
    return result


def execute(air_pressure, airport_elevation, outside_air_temp, runway_length_uncorrected, head_wind, slope_percent, aircraft_weight, AP_registration, air_conditioning, engine_anti_ice, total_anti_ice, operational_CG_percentage):
    if int(aircraft_weight) > 78.0:
        return "Max takeoff weight exceeded (over 78.0)."
        
    '''
    First thing to be done: check that the aircraft does not exceed the maximum takeoff weight. If it does, abort
    the entire program and return MTOW violation.
    
    This program does not ask for the exact model of the A320 because it hopes to be as generic as possible. Therefore,
    the MTOW used is 78,000 kg which is the maximum possible weight for all A320 models, but is specific to the 
    A320-233 variant.
    '''

    runway_length = correct_runway_length(int(runway_length_uncorrected), float(slope_percent),
                                               int(head_wind))

    best_config_array = find_best_config(int(air_pressure), int(runway_length), int(aircraft_weight))
    best_config = best_config_array[1]
    best_config_name = best_config_array[0]

    temp_ac = ac_adjustment(air_conditioning, AP_registration)

    temp_engine_ai = engine_adjustment(engine_anti_ice)
    total_anti_ice_modifier = total_anti_ice_adjustment(total_anti_ice)
    tmax_flex = calculate_tmax_flex(AP_registration, int(airport_elevation))
    flex_temp = flex_temp_adjustment(temp_engine_ai, total_anti_ice_modifier, best_config, temp_ac)

    d_qnh_adjustment = D_QNH(int(air_pressure))

    # Configuration Modifications
    flex_temp = flex_temp + d_qnh_adjustment
    best_config[0] = flex_temp

    flex_ok = flex_test(flex_temp, int(outside_air_temp))
    if not flex_ok:
        return "Flex takeoff not possible."

    # Final Corrections
    if float(operational_CG_percentage) < 27:
        best_config[0] = best_config[0] - 2
        best_config[1] = best_config[1] + 1
        best_config[2] = best_config[2] + 1
        best_config[3] = best_config[3] + 1

    # Check that V2 speed is not below the minimum
    pressure_altitude = (1 - (int(air_pressure) / 1013.25) ** 0.190284) * 145366.45  # Formula for pressure altitude
    if not v2_speed_check_is_ok(best_config[3], pressure_altitude, int(aircraft_weight), best_config_name):
        return "Flex takeoff not possible. Below minimum V2 speed."

        
    return_result = (
        best_config_name,
        "Flex Temp: " + str(best_config[0]),
        "V1: " + str(best_config[1]),
        "VR: " + str(best_config[2]),
        "V2: " + str(best_config[3])
    )

    return return_result
