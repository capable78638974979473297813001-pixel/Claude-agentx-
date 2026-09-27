import os


def resolve(root, user_path):
    return os.path.normpath(os.path.join(root, user_path))


def is_inside(root, candidate):
    return os.path.normpath(candidate).startswith(os.path.normpath(root))
