# Coding Assignment

Please write a command-line program that parses an input textual log file, extracts data from it and
saves it in a database. 

Please also write a second command line program that queries the data from the
database to extract the required statistics.

Your program may take additional parameters, as needed.

Database fields required:

File properties:
- File path (string)
- Date when file was parsed (datetime)
- Server hostname where file was parsed (string)
  

Testcase properties:
- Method API
- Method name
- Parameters (no need to parse them, just store them as string or json object)
- Execution time in seconds (floating number)


Your parser program should parse the input log file, ignore all nonmatching lines and collect above data.
It should then store the extracted data in a SQL database.

The files are produced by running a benchmark. One run can include many testcases. We assume that
same testcases (i.e. API methods) are run in multiple benchmark runs, and defined relationships should
allow to query for testcase execution times across several benchmark runs recorded in the database.
Your query program should find the average execution time for a given API method (e.g.
API.some_method) across all benchmarks performed in the last week.


# Solution

### Major Issue:
Missing data: tests execution date in time. This data will be required when computing
tests statistics.

Solution: It was decided to use naming convention for log files.
For example, the log file 2021-01-04T10-20-00.log was executed on 2021-01-04 at 10:20:00.

### Program saving the log file data to DB

**save_log_data_to_db.py** is a script that one may run from the command line

    python save_log_data_to_db.py Logs/2021-01-04T10-20-00.log

The path to the log file needs to be provided as a positional argument.


### Program calculating tests statistics

**get_statistics.py** is a script that one may run from the command line

    python get_statistics.py 2021 1

The script requires two positional parameters: tests run year and week