"""Checks for the verified skill set.

Curated tax and engineering notes are indexed, but they are not rewritten to
this bar. Every file under library/skills/ must pass schema, filler, source,
near-duplicate, and runnable-example checks.
"""

from __future__ import annotations

import json
import re
import shlex
import ssl
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from library.catalog import area_counts
from library.load import ROOT, VERIFIED_AREAS, load_verified
from library.model import Skill
from library.textutil import BANNED_PHRASES, body_hash, fences, jaccard, shingles

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
PROSE_JACCARD_LIMIT = 0.42
MIN_BODY_CHARS = 900
MIN_EXAMPLE_CHARS = 60
COMMAND_TIMEOUT_S = 90
PROSE_FENCE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)

VERSION_RE = re.compile(
    r"\b(React 19|React 18|Vue 3\.5|Svelte 5|Go 1\.2\d|Python 3\.\d+|Node\.js \d+"
    r"|Java 21|SQLite 3\.\d+|Chrome \d+|WCAG 2\.2|@testing-library/dom \d+)\b",
    re.IGNORECASE,
)


def _fence_path(info: str) -> str | None:
    for part in info.split():
        if part.startswith("file="):
            return part.split("=", 1)[1]
    return None


def validate_skill_shape(skill: Skill, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    where = skill.path or skill.id
    if skill.kind != "verified":
        return errors
    if not ID_RE.match(skill.id):
        errors.append(f"{where}: bad id {skill.id!r}")
    if skill.area not in VERIFIED_AREAS:
        errors.append(f"{where}: area {skill.area!r} is not a library area")
    expected = f"library/skills/{skill.area}/{skill.id}.md"
    if skill.path != expected:
        errors.append(f"{where}: path must be {expected}")
    if not skill.topic or not skill.task or not skill.title:
        errors.append(f"{where}: topic, task, and title are required")
    if len(skill.description) < 40:
        errors.append(f"{where}: description is too short to say when to use the skill")
    if len(skill.body) < MIN_BODY_CHARS:
        errors.append(f"{where}: body is under {MIN_BODY_CHARS} characters")
    if len(skill.triggers) < 3:
        errors.append(f"{where}: need at least 3 trigger phrases")
    if not skill.aliases:
        errors.append(f"{where}: need aliases")
    if not skill.related:
        errors.append(f"{where}: link at least one related skill")
    if skill.id in skill.related:
        errors.append(f"{where}: related list includes itself")
    if not skill.sources:
        errors.append(f"{where}: need at least one source URL")
    if not skill.commands:
        errors.append(f"{where}: need at least one command to run")
    lower = skill.body.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            errors.append(f"{where}: banned filler phrase {phrase!r}")
    if "«" in skill.body or "»" in skill.body:
        errors.append(f"{where}: leftover slot marker")
    for source in skill.sources:
        if not source.startswith("https://") and not source.startswith("http://"):
            errors.append(f"{where}: source is not a URL: {source}")
        if source not in skill.body:
            errors.append(f"{where}: source URL is not cited in the body: {source}")
    if VERSION_RE.search(skill.body) and not URL_RE.search(skill.body):
        errors.append(f"{where}: version claim without a URL in the body")
    parsed = fences(skill.body)
    file_fences = [(info, content) for info, content in parsed if _fence_path(info)]
    if len(file_fences) < 2:
        errors.append(f"{where}: need at least two file= code samples (incorrect and correct)")
    for info, content in file_fences:
        rel = _fence_path(info)
        assert rel is not None
        disk = root / rel
        if not disk.is_file():
            errors.append(f"{where}: code fence points at missing file {rel}")
            continue
        actual = disk.read_text(encoding="utf-8")
        if actual != content:
            errors.append(f"{where}: code fence does not match {rel}")
    for command in skill.commands:
        if command not in skill.body:
            errors.append(f"{where}: command is not written in the body: {command}")
    if not re.search(r"\d", skill.body):
        errors.append(f"{where}: no concrete number (version, threshold, or exit condition)")
    example_chars = sum(len(content) for info, content in file_fences)
    if example_chars < MIN_EXAMPLE_CHARS:
        errors.append(
            f"{where}: example code is under {MIN_EXAMPLE_CHARS} characters"
        )
    errors.extend(_generic_advice(skill, where))
    return errors


def _generic_advice(skill: Skill, where: str) -> list[str]:
    """Flag a body whose prose is filler or unanchored advice.

    Code fences are ignored. A long sentence counts as concrete when it
    carries a number, a backticked command or symbol, a URL, or a quote.
    """
    prose = PROSE_FENCE_RE.sub(" ", skill.body)
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", prose)
        if len(sentence.strip()) > 40
    ]
    if len(sentences) < 4:
        return [f"{where}: prose is too thin to show a failure mode"]
    anchored = [
        sentence
        for sentence in sentences
        if re.search(r"\d|`|https?://|\"[^\"]{2,}\"|'[^']{2,}'", sentence)
    ]
    if len(anchored) * 2 < len(sentences):
        return [
            f"{where}: mostly generic advice "
            f"({len(anchored)} of {len(sentences)} prose sentences name a "
            "number, command, error, or quoted fact)"
        ]
    return []


def validate_graph(skills: list[Skill]) -> list[str]:
    errors: list[str] = []
    ids = {skill.id for skill in skills}
    hashes: dict[str, str] = {}
    verified = [skill for skill in skills if skill.kind == "verified"]
    for skill in verified:
        digest = body_hash(skill.body)
        if digest in hashes:
            errors.append(f"{skill.id}: body duplicates {hashes[digest]}")
        else:
            hashes[digest] = skill.id
        for related in skill.related:
            if related not in ids:
                errors.append(f"{skill.id}: related skill {related} does not exist")
    caches = [(skill, shingles(skill.body)) for skill in verified]
    for i in range(len(caches)):
        for j in range(i + 1, len(caches)):
            score = jaccard(caches[i][1], caches[j][1])
            if score > PROSE_JACCARD_LIMIT:
                errors.append(
                    f"near-duplicate ({score:.2f}) {caches[i][0].id} vs {caches[j][0].id}"
                )
    return errors


def _fetch_status(url: str) -> tuple[str, str | None]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "skill-library-validator/1.0"},
        method="GET",
    )
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=20, context=context) as response:
            status = getattr(response, "status", 200)
            if status >= 400:
                return url, f"HTTP {status}"
            return url, None
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 429}:
            return url, None
        return url, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - report the network failure, do not invent success
        return url, str(exc)


def validate_sources(skills: list[Skill]) -> list[str]:
    urls = sorted({url for skill in skills if skill.kind == "verified" for url in skill.sources})
    errors: list[str] = []
    if not urls:
        return errors
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_fetch_status, url) for url in urls]
        for future in as_completed(futures):
            url, problem = future.result()
            if problem:
                errors.append(f"source unreachable {url}: {problem}")
    return errors


def run_commands(skills: list[Skill], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for skill in skills:
        if skill.kind != "verified":
            continue
        for command in skill.commands:
            try:
                completed = subprocess.run(
                    shlex.split(command),
                    cwd=root,
                    check=False,
                    text=True,
                    capture_output=True,
                    timeout=COMMAND_TIMEOUT_S,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"{skill.id}: command timed out: {command}")
                continue
            output = (completed.stdout or "") + (completed.stderr or "")
            if completed.returncode != 0:
                tail = output[-800:]
                errors.append(f"{skill.id}: command failed ({completed.returncode}): {command}\n{tail}")
                continue
            if "incorrect: observed" not in completed.stdout or "correct: ok" not in completed.stdout:
                errors.append(
                    f"{skill.id}: command did not report both an observed failure and a passing fix: {command}"
                )
    return errors


def validate_verified(
    skills: list[Skill] | None = None,
    *,
    root: Path = ROOT,
    run: bool = True,
    check_urls: bool = True,
) -> list[str]:
    verified = skills if skills is not None else load_verified(root)
    verified = [skill for skill in verified if skill.kind == "verified"]
    errors: list[str] = []
    for skill in verified:
        errors.extend(validate_skill_shape(skill, root))
    errors.extend(validate_graph(verified))
    if check_urls:
        errors.extend(validate_sources(verified))
    if run:
        errors.extend(run_commands(verified, root))
    return errors


def summary(skills: list[Skill]) -> dict:
    verified = [skill for skill in skills if skill.kind == "verified"]
    curated = [skill for skill in skills if skill.kind == "curated"]
    return {
        "verified": len(verified),
        "curated": len(curated),
        "total": len(skills),
        "verified_by_area": area_counts(verified),
        "curated_by_area": area_counts(curated),
    }


def dumps_summary(skills: list[Skill]) -> str:
    return json.dumps(summary(skills), indent=2)
