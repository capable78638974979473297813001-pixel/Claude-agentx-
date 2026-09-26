import sqlite3


def missing_names(connection):
    return list(connection.execute("select id from people where name != 'Ada'"))
