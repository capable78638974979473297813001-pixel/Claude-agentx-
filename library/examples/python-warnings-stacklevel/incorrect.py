import warnings


def library_call():
    warnings.warn("quota exceeded", stacklevel=1)
