# SimData Tables :: Aircraft Performance Calculator

[![SimData](https://circleci.com/gh/FrancescoAiello01/simdata-tables.svg?style=svg)](https://app.circleci.com/pipelines/github/FrancescoAiello01/simdata-tables)

Demo: [https://simdata-calculator.herokuapp.com/](https://simdata-calculator.herokuapp.com/)


This repository calculates aircraft takeoff performance using tables extracted from the A320 FCOM based on input parameters.

Originally, this repository was private, but is now public. It is still in the process of major refactoring and some areas of the code may not be clean or clear.

## Installation

Python 3 is required.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt:

```bash
$ pip install -r requirements.txt
$ gunicorn main:app
```

## Contributing

Pull requests are welcome.

## License

Copyright Francesco Aiello 2020
