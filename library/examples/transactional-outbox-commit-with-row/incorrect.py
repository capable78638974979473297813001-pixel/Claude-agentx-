def place(connection, should_fail):
    connection.execute("insert into orders(id) values (1)")
    connection.commit()
    if should_fail:
        raise RuntimeError("publisher down")
    connection.execute("insert into outbox(order_id) values (1)")
    connection.commit()
