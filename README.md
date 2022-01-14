# parse-dswd-dromic-reports
Parse tables in DSWD-DROMIC reports to csv. Built in support to typhoon Rai (2021).

Latest DSWD-DROMIC reports can be obtained [here](https://dromic.dswd.gov.ph/). 

### Requirements
- [Python > 3.7](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/getting-started/)

### Setup
```
pip install requirements.txt
```

### Usage
```
Usage: parse-report.py [OPTIONS]

Options:
  --report TEXT  report to parse (.docx)
  --dest TEXT    output directory
  --help         Show this message and exit
  ```
