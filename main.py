#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One-Star Review of Something Essential — entry writer.

The competition asks for one single-line, deadpan one-star review of
an everyday essential, at most 160 characters, written to
/output/entry.txt. This entry reviews sleep.

The review is assembled from three grievance beats, each one a true
and specific complaint about sleep, filed in earnest:

  1. the tariff — it takes eight hours a night, every night;
  2. the fine print — it punishes both too much and too little;
  3. the walkout — it quits entirely the night before anything
     important, which is the turn the whole line is read straight for.

Revision note: the first draft spelled the rating out ("One star")
and let the walkout arrive as a refusal to "show up". The shipped
line uses the review-native "1 star", swaps the vaguer "demands" for
the concrete "takes", and lands the walkout with "quits entirely" —
ten code points shorter and the sting sits in the last clause.

The program is deterministic: it joins the beats, checks the result
against the gate's contract (1 to 160 code points, single line,
non-blank), writes it with no trailing newline, then reads the file
back and compares, so a run either produces exactly the intended
bytes or fails loudly.

MAKEFUN_OUTPUT_DIR redirects the output directory for local test
runs; the grader's default is /output/entry.txt.
"""

import os
import pathlib

RATING = "1 star for sleep."
BEATS = (
    "It takes eight hours a night,",
    "punishes both too much and too little,",
    "and quits entirely the night before anything important.",
)

MAX_CODE_POINTS = 160
DEFAULT_OUTPUT = pathlib.Path("/output/entry.txt")


def render() -> str:
    """Assemble the review: the rating, then the grievances in order."""
    return " ".join((RATING, *BEATS))


def check(text: str) -> None:
    """Raise unless the text satisfies the gate: 1..160 chars, one line."""
    if not 1 <= len(text) <= MAX_CODE_POINTS:
        raise ValueError(f"entry is {len(text)} code points, need 1..{MAX_CODE_POINTS}")
    if text != text.strip() or not text.strip():
        raise ValueError("entry must be non-blank with no surrounding white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def target_path() -> pathlib.Path:
    """MAKEFUN_OUTPUT_DIR redirects the output dir for local test runs."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return pathlib.Path(override) / "entry.txt"
    return DEFAULT_OUTPUT


def main() -> None:
    entry = render()
    check(entry)
    path = target_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(entry.encode("utf-8"))
    if path.read_bytes() != entry.encode("utf-8"):
        raise RuntimeError("written entry does not match the intended bytes")


if __name__ == "__main__":
    main()
