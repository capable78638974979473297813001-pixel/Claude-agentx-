def create(connection):
    connection.execute("create table events(id integer primary key, user_id integer)")
