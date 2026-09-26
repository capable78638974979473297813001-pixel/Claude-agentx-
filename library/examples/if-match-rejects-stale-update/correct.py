def update(row, new_name, client_version):
    if row["version"] != client_version:
        return 412
    row["name"] = new_name
    row["version"] += 1
    return 200
