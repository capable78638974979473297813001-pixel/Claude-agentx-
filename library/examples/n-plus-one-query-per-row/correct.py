def load_orders(connection, user_ids):
    marks = ",".join("?" for _ in user_ids)
    return connection.execute(
        f"select id from orders where user_id in ({marks})",
        tuple(user_ids),
    ).fetchall()
