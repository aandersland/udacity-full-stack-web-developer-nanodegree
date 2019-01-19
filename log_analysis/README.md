## Overview
The Log Analysis project is focused on building an internal reporting tool for a newspaper site. We have a database with
over a million rows provided by Udacity that contains newspaper articles and web server logs.

The report script will be written in Python and SQL. All the heavy lifting will be done by the database. The script will be used for orchestration and minimal formating.

The report will answer the following questions according to the format in the examples below.

1. What are the most popular three articles of all time? 
* Example: "Princess Shellfish Marries Prince Handsome" — 1201 views

2. Who are the most popular article authors of all time? 
* Example: Ursula La Multa — 2304 views

3. On which days did more than 1% of requests lead to errors? 
* Example: July 29, 2016 — 2.5% errors

## How to run the script
You will need the following installed on your machine: 
1. A linux based virtual machine if you do not have linux -  https://www.vagrantup.com/
2. Postgress installed on the virtual machine
3. A copy of the news data from the Udacity classroom loaded into the database
4. The log_analysis.py script in this repository.

Once you have the initial setup complete simply run the script (python log_analysis.py)


## Resources
* https://www.postgresql.org/docs/9.1/functions-formatting.html
* http://www.postgresqltutorial.com/postgresql-date/
* https://dba.stackexchange.com/questions/69108/postgresql-using-count-to-determine-percentages-cast-issues
* https://www.python.org/dev/peps/pep-0263/
* https://stackoverflow.com/questions/6454146/getting-the-encoding-of-a-postgres-database
* https://www.programiz.com/python-programming/methods/string/encode
