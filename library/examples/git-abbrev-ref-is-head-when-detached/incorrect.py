import subprocess


def branch_name(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
