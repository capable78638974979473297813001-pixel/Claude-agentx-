import os


def resolve(root, user_path):
    root_real = os.path.realpath(root)
    candidate = os.path.realpath(os.path.join(root, user_path))
    if os.path.commonpath([root_real, candidate]) != root_real:
        raise ValueError("path escapes root")
    return candidate
