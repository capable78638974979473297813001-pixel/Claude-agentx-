import argparse


def parse(argv):
    parser = argparse.ArgumentParser(prog="tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("cmd")
    parser.add_argument("args", nargs="*")
    return parser.parse_args(argv)
