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

## Setup
You will need the following installed on your machine: 
1. Install VirtualBox - https://www.virtualbox.org/wiki/Downloads
2. A linux based virtual machine if you do not have linux -  https://www.vagrantup.com/
4. A copy of the news data from the Udacity classroom loaded into the database located in this repository. This will need to be unzipped.
5. A copy of the Vagrant file from Udacity located in this repository.
6. The log_analysis.py script in this repository.
7. Your folder structure should look like the example below.
8. Once your folders are setup navigate to the root_folder and run the command **vagrant up** to setup your virtual machine.
9. After it finishes installing the components you can run **vagrant ssh** to access the virtual machine.
10. Once in the vm run **cd /vagrant**. This will navigate to the shared folder on your computer where the files are located.
11. Next run this command ** psql -d news -f newsdata.sql** to load the data into the news database.
12. Finally run the command **./log_analysis.py** to execute the script and get the results. Python 2.7 was used in the creation of this script.

## Folder Structure
 * root_folder/
 * root_folder/news/newsdata.sql
 * root_folder/log_analysis.py
 * root_folder/Vagrantfile

## Resources
* https://www.postgresql.org/docs/9.1/functions-formatting.html
* http://www.postgresqltutorial.com/postgresql-date/
* https://dba.stackexchange.com/questions/69108/postgresql-using-count-to-determine-percentages-cast-issues
* https://www.python.org/dev/peps/pep-0263/
* https://stackoverflow.com/questions/6454146/getting-the-encoding-of-a-postgres-database
* https://www.programiz.com/python-programming/methods/string/encode
