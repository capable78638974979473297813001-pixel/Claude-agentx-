import sqlite3


def connect():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table parent(id integer primary key)")
    connection.execute(
        "create table child(id integer primary key, parent_id integer references parent(id))"
    )
    connection.execute("insert into parent(id) values (1)")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("insert into child(parent_id) values (99)")
    return connection
