def update(row, new_name, client_version):
    row["name"] = new_name
    row["version"] += 1
    return 200
