def create(connection):
    connection.execute("create table events(id integer primary key, user_id integer)")
    connection.execute("create index events_user_id on events(user_id)")
