import sqlite3


def connect():
    connection = sqlite3.connect(":memory:")
    connection.isolation_level = None
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("create table parent(id integer primary key)")
    connection.execute(
        "create table child(id integer primary key, parent_id integer references parent(id))"
    )
    return connection
