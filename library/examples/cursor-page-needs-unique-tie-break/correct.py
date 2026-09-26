def page(rows, limit, cursor):
    ordered = sorted(rows, key=lambda row: (row["created"], row["id"]))
    if cursor is None:
        return ordered[:limit]
    return [row for row in ordered if (row["created"], row["id"]) > cursor][:limit]
