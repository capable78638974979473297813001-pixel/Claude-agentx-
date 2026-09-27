def find_user(connection, name):
    return list(connection.execute("select id from users where name = ?", (name,)))
