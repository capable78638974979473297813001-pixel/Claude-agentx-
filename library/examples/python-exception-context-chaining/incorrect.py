def convert(raw):
    try:
        int(raw)
    except ValueError:
        raise RuntimeError("bad token")
