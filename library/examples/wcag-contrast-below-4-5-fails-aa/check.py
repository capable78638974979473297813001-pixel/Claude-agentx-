import importlib.util
import pathlib

root = pathlib.Path(__file__).parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bad = load("incorrect")
good = load("correct")
gray = (128, 128, 128)
white = (255, 255, 255)
bad_gray = bad.contrast_ratio(gray, white)
good_gray = good.contrast_ratio(gray, white)
if bad_gray > 2 or good_gray < 3.5:
    raise SystemExit((bad_gray, good_gray))
print("incorrect: observed", round(bad_gray, 2))

black_white = good.contrast_ratio((0, 0, 0), white)
if abs(black_white - 21) > 0.001:
    raise SystemExit(black_white)
if abs(good_gray - 3.9494396480491156) > 0.001:
    raise SystemExit(good_gray)
if not good.passes_normal_text_aa((118, 118, 118), white):
    raise SystemExit("rgb(118,118,118) should pass 4.5:1")
if good.passes_normal_text_aa((119, 119, 119), white):
    raise SystemExit("rgb(119,119,119) should fail 4.5:1")
print("correct: ok", round(black_white, 1))
