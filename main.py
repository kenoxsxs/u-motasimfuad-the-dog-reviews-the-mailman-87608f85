"""One-line dog review of the mailman.

Writes a single-line review to $MAKEFUN_OUTPUT_DIR/entry.txt.
Standard library only.
"""

import hashlib
import os
from pathlib import Path

DOG_REVIEW = "One star. He comes every day, teases me through the gate, and never once brings the package inside. I will bark. I have always barked."


def review(line):
    """Check a review line: one line, not blank, 1 to 200 characters."""
    if "\n" in line or "\r" in line:
        raise ValueError("review must be a single line")
    if not line.strip():
        raise ValueError("review must not be only whitespace")
    if not 1 <= len(line) <= 200:
        raise ValueError("review must be 1 to 200 characters")
    return line


def gate_dir():
    """Resolve the output folder from the environment."""
    return Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))


def bark_review(folder, line):
    """Write the review to entry.txt with exclusive creation."""
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    if target.exists():
        target.unlink()
    payload = line.encode("utf-8")
    with target.open("x", encoding="utf-8") as handle:
        handle.write(line)
    return target, payload


def check_review(target, payload):
    """Read the file back and confirm it matches the payload exactly."""
    stored = target.read_bytes()
    if stored != payload:
        raise ValueError("written bytes do not match the review")
    if stored.decode("utf-8") != DOG_REVIEW:
        raise ValueError("written text does not match the review")
    if stored != stored.rstrip():
        raise ValueError("written text has trailing whitespace")
    return stored


def deliver_review():
    """Write the review, verify it, and print its digest."""
    line = review(DOG_REVIEW)
    folder = gate_dir()
    target, payload = bark_review(folder, line)
    stored = check_review(target, payload)
    digest = hashlib.sha256(stored).hexdigest()
    print("barked:", target, "|", len(stored), "bytes | sha256", digest)


if __name__ == "__main__":
    deliver_review()
