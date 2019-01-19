#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import psycopg2


def get_db_connect(_database_name):
    """
    Create a database connection to the news database and return a cursor.

    :param _database_name:
    :return: a database connection and a cursor
    """
    _db = psycopg2.connect('dbname='+_database_name)
    _cursor = _db.cursor()
    return _db, _cursor


# method to get results
def execute_query(_db_cursor, _query):
    """
    Runs a sql query and returns the results.
    :param _db_cursor: A cursor to a database.
    :param _query: A SQL query.
    :return: A list of tuples.
    """
    _db_cursor.execute(_query)
    _results = _db_cursor.fetchall()
    return _results


def print_top_articles(_cursor):
    """
    Print out the top 3 articles of all time.
    :param _cursor: A cursor to a database.
    :return:
    """
    _query = """
        SELECT a.title, count(l.path)
        FROM log AS l
        JOIN articles AS a ON a.slug = substring(l.path, 10)
        GROUP BY a.title having length(a.title) > 1
        order by count(a.title) desc
        limit 3;
        """
    _data = execute_query(_cursor, _query)

    print('\n')
    print('1. What are the most popular three articles of all time?')
    for _record in _data:
        print('"{}" - {} views'.format(_record[0].encode('UTF8'), _record[1]))


def print_top_authors(_cursor):
    """
    Print out the most popular authors of all time.
    :param _cursor: A cursor to a database.
    :return:
    """
    _query = """
        SELECT au.name, count(l.path)
        FROM authors AS au
        JOIN articles AS ar ON ar.author = au.id
        JOIN log AS l ON substring(l.path, 10) = ar.slug
        GROUP BY au.name
        order by count(l.path) desc;
        """
    _data = execute_query(_cursor, _query)

    print('\n')
    print('2. Who are the most popular article authors of all time?')
    for _record in _data:
        print('{} - {} views'.format(_record[0].encode('UTF8'), _record[1]))


def print_errors_over_one(_cursor):
    """
    Print out error connections over 1 percent.
    :param _cursor:
    :return:
    """
    _query = """
        SELECT to_char(a.time::date, 'FMMONTH dd, yyyy'),
        round((count(b.status)*100)::numeric/count(a.status), 2) error_rate
        FROM log AS a
        LEFT JOIN log AS g ON g.id = a.id and g.status = '200 OK'
        LEFT JOIN log AS b ON b.id = a.id and b.status = '404 NOT FOUND'
        GROUP BY a.time::date
        HAVING round((count(b.status)*100)::numeric/count(g.status), 2) > 1;
        """
    _data = execute_query(_cursor, _query)

    print('\n')
    print('3. On which days did more than 1% of requests lead to errors?')
    for _record in _data:
        print('{} - {}% errors'.format(_record[0].encode('UTF8'), _record[1]))


if __name__ == '__main__':
    conn, cursor = get_db_connect('news')
    print_top_articles(cursor)
    print_top_authors(cursor)
    print_errors_over_one(cursor)
    conn.close()
print('\n')
