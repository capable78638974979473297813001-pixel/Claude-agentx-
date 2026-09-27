def page(rows, limit, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    if cursor is None:
        return ordered[:limit]
    created, _row_id = cursor
    return [row for row in ordered if row["created"] > created][:limit]
