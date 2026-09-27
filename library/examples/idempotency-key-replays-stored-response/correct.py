def post(store, key, handler):
    if key in store:
        return store[key]
    body = handler()
    store[key] = body
    return body
