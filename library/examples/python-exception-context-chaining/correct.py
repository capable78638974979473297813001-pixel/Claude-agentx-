def convert(raw):
    try:
        int(raw)
    except ValueError as exc:
        raise RuntimeError("bad token") from exc
