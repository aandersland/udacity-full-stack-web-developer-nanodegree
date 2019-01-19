#!/user/bin/env python3
# -*- coding: UTF-8 -*-

import psycopg2

# setup database connection
db = psycopg2.connect('dbname=news')
cursor = db.cursor()


# method to get results
def get_results(_str):
    cursor.execute(_str)
    results = cursor.fetchall()
    return results


# question 1
query = "select a.title, count(l.path) from log l join articles a on a.slug = substring(l.path, 10) " \
    "group by a.title having length(a.title) > 1 order by count(a.title) desc  limit 3;"
data = get_results(query)

print('\n')
print('1. What are the most popular three articles of all time?')
for record in data:
    print('"{}" - {} views'.format(record[0].encode('UTF8'), record[1]))

# question 2
query = "select au.name, count(l.path) from authors au join articles ar on ar.author = au.id " \
    "join log l on substring(l.path, 10) = ar.slug group by au.name order by count(l.path) desc;"
data = get_results(query)

print('\n')
print('2. Who are the most popular article authors of all time?')
for record in data:
    print('{} - {} views'.format(record[0].encode('UTF8'), record[1]))

# question 3
query = "select to_char(a.time::date, 'FMMONTH dd, yyyy'), round((count(b.status)*100)::numeric/count(g.status), 1) " \
    "error_rate from log a left join log g on g.id = a.id and g.status = '200 OK' left join log b on b.id = a.id " \
        "and b.status = '404 NOT FOUND' group by a.time::date " \
        "having round((count(b.status)*100)::numeric/count(g.status), 1) > 1;"
data = get_results(query)

print('\n')
print('3. On which days did more than 1% of requests lead to errors?')
for record in data:
    print('{} - {}% errors'.format(record[0].encode('UTF8'), record[1]))

db.close()
print('\n')
