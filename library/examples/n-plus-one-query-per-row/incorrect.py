def load_orders(connection, user_ids):
    orders = []
    for user_id in user_ids:
        orders.extend(
            connection.execute(
                "select id from orders where user_id = ?",
                (user_id,),
            ).fetchall()
        )
    return orders
