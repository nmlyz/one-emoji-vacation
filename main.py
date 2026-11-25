#!/usr/bin/env python3
"""Write one emoji to /output/entry.txt.

The emoji is the one emoji for a dream vacation: Mount Fuji.
A snow-capped mountain is the trip itself in a single picture: the
brief names a mountain as a dream vacation, and this one mountain
names one particular dream, a journey to Japan, instead of any
holiday. The shape is a postcard at a glance and reads at any size.

Behaviour
----------
* Writes exactly one emoji, Mount Fuji, as UTF-8 bytes to
  ``/output/entry.txt`` (or ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when that
  environment variable is set).
* The file contains the emoji only: four bytes, no trailing newline.
* Standard library only, no network access, no randomness.
* Deterministic: every run writes byte-identical output.

Validation
----------
Before writing, the emoji is checked against the competition's entry
rules: it must be a single character of 1-8 characters, contain no
whitespace, and be exactly one emoji (a single code point in the
emoji ranges). An emoji that fails any of these checks is rejected
with a descriptive error and nothing is written.
"""

import os
import sys
import unicodedata
from pathlib import Path

EMOJI = "🗻"

MIN_LENGTH = 1
MAX_LENGTH = 8
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_DIR_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
FILE_MODE = 0o644


def is_emoji_character(character):
    """Return True when *character* is a single emoji code point.

    Emoji code points live in a handful of Unicode blocks; the check
    covers the pictograph, symbol and dingbat ranges used by ordinary
    emoji, plus the transport and map symbols. A variation selector
    (U+FE00-U+FE0F) or a zero-width joiner (U+200D) is not an emoji on
    its own, so neither range counts here.
    """
    code = ord(character)
    if code == 0x200D or 0xFE00 <= code <= 0xFE0F:
        return False
    ranges = (
        (0x1F000, 0x1FAFF),
        (0x2600, 0x27BF),
        (0x2190, 0x21FF),
        (0x2300, 0x23FF),
        (0x2B00, 0x2BFF),
    )
    return any(start <= code <= end for start, end in ranges)


def validate_emoji(emoji):
    """Check *emoji* against the entry rules, returning a list of problems.

    An empty list means the emoji is a valid entry. Each problem is a
    short human-readable sentence naming the rule that failed, so a
    caller can report exactly what is wrong instead of a bare failure.
    """
    problems = []
    if not isinstance(emoji, str):
        problems.append("entry must be text, got %s" % type(emoji).__name__)
        return problems
    if not emoji:
        problems.append("entry must not be empty")
        return problems
    if len(emoji) < MIN_LENGTH or len(emoji) > MAX_LENGTH:
        problems.append(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(emoji))
        )
    if emoji.strip() != emoji:
        problems.append("entry must not have leading or trailing whitespace")
    if any(character.isspace() for character in emoji):
        problems.append("entry must not contain whitespace")
    if len(emoji) != 1:
        problems.append(
            "entry must be exactly one emoji, got %d characters" % len(emoji)
        )
    elif not is_emoji_character(emoji):
        problems.append("entry must be a single emoji character")
    if unicodedata.category(emoji[0]).startswith("C"):
        problems.append("entry must not be a control character")
    return problems


def resolve_output_dir():
    """Return the directory the entry file is written to.

    ``$MAKEFUN_OUTPUT_DIR`` wins when it is set to a non-empty value;
    otherwise the default ``/output`` is used. The directory is created
    (including parents) when it does not already exist.
    """
    raw = os.environ.get(OUTPUT_DIR_ENV_VAR, "")
    directory = Path(raw) if raw.strip() else Path(DEFAULT_OUTPUT_DIR)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def encode_entry(emoji):
    """Encode *emoji* exactly as it must appear in the entry file."""
    return emoji.encode("utf-8")


def write_entry(emoji, directory):
    """Write *emoji* to ``entry.txt`` inside *directory* and return its path.

    The file is written in binary mode with no newline translation, so
    the bytes on disk are exactly the UTF-8 encoding of the emoji.
    """
    path = directory / OUTPUT_FILENAME
    data = encode_entry(emoji)
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, FILE_MODE)
    return path


def verify_entry(path, emoji):
    """Read the entry file back and check it holds exactly *emoji*.

    Returns a list of problems (empty when the file is correct). This
    read-back catches a truncated write, a stray newline, or an
    encoding surprise before the run can report success.
    """
    problems = []
    expected = encode_entry(emoji)
    try:
        actual = path.read_bytes()
    except OSError as exc:
        problems.append("could not read back %s: %s" % (path, exc))
        return problems
    if actual != expected:
        problems.append(
            "read-back mismatch in %s: expected %d bytes %r, found %d bytes %r"
            % (path, len(expected), expected, len(actual), actual)
        )
    return problems


def main(argv=None):
    """Validate the emoji, write the entry file, verify it, and report."""
    problems = validate_emoji(EMOJI)
    if problems:
        for problem in problems:
            print("error: entry %r is invalid: %s" % (EMOJI, problem), file=sys.stderr)
        return 1
    directory = resolve_output_dir()
    path = write_entry(EMOJI, directory)
    problems = verify_entry(path, EMOJI)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        print(
            "error: entry file %s failed verification; "
            "nothing was accepted as the entry" % path,
            file=sys.stderr,
        )
        return 1
    print("wrote %r (%d bytes) to %s" % (EMOJI, len(encode_entry(EMOJI)), path))
    print("verified: %s holds exactly %r, no trailing newline" % (path, EMOJI))
    return 0


if __name__ == "__main__":
    sys.exit(main())
