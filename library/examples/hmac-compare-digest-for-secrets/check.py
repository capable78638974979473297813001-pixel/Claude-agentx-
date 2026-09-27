import hmac
import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect").tokens_match
if bad("secret", "secret") is not True or bad("secret", "secreT") is not False:
    raise SystemExit("equality helper returned an unexpected bool")
try:
    hmac.compare_digest(b"secret", "secret")
except TypeError as exc:
    print("incorrect: observed", type(exc).__name__)
else:
    raise SystemExit("mixed types were accepted by compare_digest")

good = load("correct").tokens_match
if good("secret", "secret") is not True or good("secret", "secreT") is not False:
    raise SystemExit("compare_digest wrapper disagrees with equality")
if good(b"secret", "secret") is not True:
    raise SystemExit("str/bytes normalization failed")
print("correct: ok")
