# SimData Tables :: Aircraft Performance Calculator

[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/FrancescoAiello01/simdata-tables/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/FrancescoAiello01/simdata-tables/test_coverage)
[![CircleCI](https://circleci.com/gh/FrancescoAiello01/simdata-tables.svg?style=svg)](https://app.circleci.com/pipelines/gh/FrancescoAiello01/simdata-tables)
[![codecov](https://codecov.io/gh/FrancescoAiello01/simdata-tables/branch/master/graph/badge.svg)](https://codecov.io/gh/FrancescoAiello01/simdata-tables)

This is the root repository for the SimData.io backend. Everything here is the actual Python functionality in the API. It was chosen to separate this into it's own repository for more maintainability as the project grows.

This repository calculates aircraft takeoff performance using tables extracted from the A320 FCOM (flight crew operations manual).

Originally, this repository was private, but is now public. It is still in the process of major refactoring and some areas of the code may not be clean or clear.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install scipy
pip install numpy
pip install pandas
pip install xlrd
```

## Usage

```
# Test input:
python calculator_production.py --air_pressure 990 --airport_elevation 1000 --outside_air_temp 35 --runway_length_uncorrected 2750 --head_wind 10 --slope_percent 1 --aircraft_weight 66 --AP_registration False --air_conditioning False --engine_anti_ice True --total_anti_ice False --operational_CG_percentage 26
```

Command line arguments are inputted as follows "--argument value". Here are the required values to be inputted:

- air_pressure in hPa
- airport_elevation in feet
- outside_air_temp in C
- runway length in feet
- head_wind
- runway slope percentage (uphill is positive, downhill is negative)')
- aircraft_weight (example 66 for 66,000)
- Registration is AP-BLY or AP-BLZ
- air_conditioning boolean
- engine_anti_ice boolean
- total_anti_ice boolean
- operational_CG_percentage integer

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Copyright Francesco Aiello / Aiello Holdings LLC. All rights reserved.
