import subprocess


def describe(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "describe", "--tags"],
        check=False,
        text=True,
        capture_output=True,
    )
