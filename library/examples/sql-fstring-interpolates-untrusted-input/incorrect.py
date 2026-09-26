def find_user(connection, name):
    return list(connection.execute(f"select id from users where name = '{name}'"))
