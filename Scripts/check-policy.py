#!/usr/bin/env python3
"""Check event commit messages, PR titles and added source lines."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import Request, urlopen


TYPES = "build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
SUBJECT = re.compile(rf"(?:{TYPES})(?:\([^()\r\n]+\))?!?: \S[^\r\n]*")
ATTRIBUTION = re.compile(
    r"^\s*(?:Co-authored-by|Signed-off-by|Generated-by|Generated-with|"
    r"Made-with|Assisted-by|Powered-by):", re.IGNORECASE | re.MULTILINE
)
DEPENDABOT_SIGNOFF = "Signed-off-by: dependabot[bot] <support@github.com>"
CONFLICT = re.compile(r"^(?:<{7}(?: |$)|={7}$|>{7}(?: |$)|\|{7}(?: |$))")
ZERO = "0" * 40


def git(*arguments):
    return subprocess.check_output(
        ["git", *arguments], text=True, errors="replace", stdin=subprocess.DEVNULL
    )


def message_findings(label, message, *, dependabot=False):
    subject = message.split("\n", 1)[0]
    findings = []
    if not SUBJECT.fullmatch(subject) or subject != subject.rstrip():
        findings.append(f"{label}: expected a Conventional Commit subject ({TYPES})")
    if any(ATTRIBUTION.search(line) and not (dependabot and line == DEPENDABOT_SIGNOFF)
           for line in message.split("\n")):
        findings.append(f"{label}: forbidden attribution trailer")
    return findings


def authenticated_dependabot_commit(repository, commit):
    """Require GitHub's verified bot identity, not a spoofable Git author field."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("invalid repository for commit authentication")
    request = Request(
        f"https://api.github.com/repos/{repository}/commits/{commit}",
        headers={"Accept": "application/vnd.github+json",
                 "Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "X-GitHub-Api-Version": "2022-11-28"},
        method="GET",
    )
    with urlopen(request, timeout=30) as response:
        observed = json.load(response)
    if not isinstance(observed, dict):
        return False
    author = observed.get("author") or {}
    committer = observed.get("committer") or {}
    details = observed.get("commit") or {}
    if not all(isinstance(value, dict) for value in (author, committer, details)):
        return False
    verification = details.get("verification") or {}
    if not isinstance(verification, dict):
        return False
    # A verified signature by a different contributor does not authenticate
    # a claimed bot author. Dependabot commits use GitHub's web-flow signer.
    return (observed.get("sha") == commit
            and author.get("login") == "dependabot[bot]" and author.get("type") == "Bot"
            and committer.get("login") == "web-flow"
            and verification.get("verified") is True and verification.get("reason") == "valid")


def added_findings(patch, *, trailing_blank_start=None):
    """Inspect hunk additions, including additions whose text starts with '++'."""
    findings = []
    path = "diff"
    number = None
    for line in patch.split("\n"):
        if line.startswith("diff --git "):
            path, number = line, None
        elif line.startswith("+++ ") and number is None:
            path = line[4:]
        elif match := re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line):
            number = int(match[1])
        elif number is not None and line.startswith("+"):
            content = line[1:]
            if content.rstrip(" \t\r") != content or re.match(r"^[ \t]* \t", content):
                findings.append(f"{path}:{number}: whitespace error")
            if trailing_blank_start is not None and number >= trailing_blank_start and not content.strip():
                findings.append(f"{path}:{number}: added blank line at end of file")
            if CONFLICT.match(content):
                findings.append(f"{path}:{number}: conflict marker")
            if ATTRIBUTION.search(content):
                findings.append(f"{path}:{number}: forbidden attribution trailer")
            number += 1
        elif number is not None and line.startswith(" "):
            number += 1
    return findings


def source_range(event, event_name):
    if event_name == "pull_request":
        base = event["pull_request"]["base"]["sha"]
        head = event["pull_request"]["head"]["sha"]
    elif event_name == "workflow_dispatch":
        base, head = None, os.environ["GITHUB_SHA"]
    elif event_name == "push" and not event.get("deleted"):
        base, head = event["before"], event["after"]
        if not re.fullmatch(r"[0-9a-f]{40}", head) or head == ZERO:
            raise ValueError("policy requires a full, nonzero head commit SHA")
        if base == ZERO:
            # New topic branches compare with the fetched default branch, so
            # published legacy ancestors are outside the new-work policy.
            default = event["repository"]["default_branch"]
            default_head = git("rev-parse", "refs/remotes/origin/" + default).strip()
            base = git("merge-base", default_head, head).strip()
    else:
        raise ValueError("policy requires a pull_request, workflow_dispatch or non-deletion push")
    commits = (head,) if event_name == "workflow_dispatch" else (base, head)
    if any(not re.fullmatch(r"[0-9a-f]{40}", value) or value == ZERO for value in commits):
        raise ValueError("policy requires full, nonzero source commit SHAs")
    return base, head


def check(event, event_name):
    base, head = source_range(event, event_name)
    findings = []
    if event_name == "pull_request":
        title = event["pull_request"]["title"]
        if "\n" in title or "\r" in title:
            findings.append("PR title: expected a single line")
        findings.extend(message_findings("PR title", title))
        comparison = git("merge-base", base, head).strip()
    else:
        comparison = base
    commits = [head] if base is None else git("rev-list", "--reverse", base + ".." + head).splitlines()
    for commit in commits:
        # Preserve carriage returns: newline normalization would broaden the
        # exact signoff exception to differently spelled trailer lines.
        message = subprocess.check_output(
            ["git", "show", "-s", "--format=%B", commit], stdin=subprocess.DEVNULL
        ).decode("utf-8", errors="replace")
        dependabot = (DEPENDABOT_SIGNOFF in message.split("\n")
                      and authenticated_dependabot_commit(event["repository"]["full_name"], commit))
        findings.extend(message_findings(commit, message, dependabot=dependabot))
    if comparison is None:
        # Dispatch supplies a selected commit but no new-change range.
        return findings
    paths = git("diff", "--name-only", "--no-renames", "--diff-filter=ACMT", "-z",
                comparison, head, "--").split("\0")
    for path in filter(None, paths):
        if git("--literal-pathspecs", "ls-tree", head, "--", path).startswith("160000 "):
            continue
        blob = subprocess.check_output(["git", "cat-file", "blob", head + ":" + path])
        # Determine binary content ourselves; consumer attributes cannot hide
        # text from the pinned checker or disable its whitespace rules.
        if b"\0" in blob[:8000]:
            continue
        lines = blob.decode("utf-8", errors="replace").splitlines()
        trailing_blank_start = len(lines) + 1
        while trailing_blank_start > 1 and not lines[trailing_blank_start - 2].strip():
            trailing_blank_start -= 1
        patch = git("--literal-pathspecs", "diff", "--text", "--no-ext-diff", "--no-textconv", "--no-color", "--no-renames",
                    "--unified=0", comparison, head, "--", path)
        findings.extend(added_findings(patch, trailing_blank_start=trailing_blank_start))
    return findings


def main():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    findings = check(event, os.environ["GITHUB_EVENT_NAME"])
    # Avoid interpreting source-controlled text as workflow commands.
    for finding in findings:
        print("FAIL " + finding.replace("\n", " | "))
    if not findings:
        print("PASS source policy")
    return int(bool(findings))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"FAIL policy could not complete: {type(error).__name__}", file=sys.stderr)
        sys.exit(1)
