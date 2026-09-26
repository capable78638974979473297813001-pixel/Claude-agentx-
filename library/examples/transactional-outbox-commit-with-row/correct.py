def place(connection, should_fail):
    try:
        connection.execute("insert into orders(id) values (1)")
        connection.execute("insert into outbox(order_id) values (1)")
        if should_fail:
            raise RuntimeError("publisher down")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
