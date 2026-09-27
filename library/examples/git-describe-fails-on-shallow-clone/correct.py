import subprocess


def describe(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "describe", "--tags"],
        check=True,
        text=True,
        capture_output=True,
    )
