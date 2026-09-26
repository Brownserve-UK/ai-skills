#!/usr/bin/env python3
"""Check text against the Plain Technical English rules that a script can test.

Usage:
    python3 check.py [--spelling british] [--allow WORD,WORD] FILE [FILE ...]
    cat FILE | python3 check.py -

The script ignores fenced code blocks, inline code, URLs, and file paths.
It reports two kinds of result:
    ERROR  - a rule violation. Correct it. The exit code becomes 1.
    WARN   - a possible violation that needs a human decision.

Rules the script tests (rule numbers refer to ASD-STE100 Issue 8, Part 1):
    ERROR  no semicolons                                  (8.1)
    ERROR  no em dashes                                   (house style)
    ERROR  no contractions                                (4.2)
    ERROR  no sentence with more than 25 words            (5.1, 6.3)
    ERROR  no unapproved word from the table below        (1.1, 1.2, 9.2)
    ERROR  no spelling from the other variant of English  (1.14, relaxed)
    WARN   sentence with 21 to 25 words (limit 20 for instructions)
    WARN   "-ing" word that is not a known technical name (3.5)
    WARN   possible passive voice                         (3.6)
    WARN   paragraph with more than six sentences         (6.6)

The word table is small. It holds the words that appear most often in
software text and that the STE dictionary does not approve. Pass the
technical names of your domain with --allow or --allow-file when the script
reports them.
"""

import argparse
import bisect
import re
import sys

# Unapproved word -> approved alternative. Keys are lowercase lemmas.
# Source: ASD-STE100 Issue 8, Part 2 (Dictionary).
UNAPPROVED = {
    "acceptable": "permitted",
    "afterwards": "after that",
    "amount": "quantity",
    "approach": "method",
    "ask": "write the question directly, or use 'tell'",
    "attempt": "try",
    "choice": "selection",
    "combine": "mix, or put together",
    "consider": "think about",
    "could": "can",
    "cross": "go across",
    "detail": "instruction, or give",
    "ensure": "make sure",
    "exact": "accurate",
    "expect": "think, or possible",
    "explain": "tell, or give the cause",
    "fail": "does not",
    "grow": "become",
    "however": "but",
    "indicate": "show",
    "instead": "as an alternative",
    "later": "subsequent, after",
    "maintain": "keep",
    "major": "primary",
    "may": "can",
    "might": "can",
    "minor": "small",
    "never": "do not",
    "now": "at this time",
    "obvious": "clear",
    "often": "many times",
    "omit": "do not do, do not write",
    "option": "alternative",
    "past": "more than, after",
    "permit": "let",
    "prefer": "recommend",
    "priority": "important",
    "provide": "give",
    "purpose": "function",
    "question": "ask directly, or use 'check'",
    "reach": "get",
    "reason": "cause",
    "require": "must, necessary",
    "serious": "important",
    "several": "some",
    "severe": "dangerous",
    "should": "must",
    "suggest": "recommend",
    "suggestion": "recommendation",
    "therefore": "as a result",
    "understand": "know",
    "whole": "full",
    "why": "what is the cause",
    "would": "can, will",
    "wrong": "incorrect",
}

# "-ing" words that are nouns, technical names, or plain words. No warning.
TECHNICAL_ING_WORDS = {
    "anything", "bring", "caching", "casting", "during", "encoding",
    "everything", "formatting", "handling", "hiding", "king", "linting",
    "loading", "logging", "mapping", "matching", "meaning", "monitoring",
    "morning", "nesting", "nothing", "parsing", "rendering", "ring",
    "routing", "setting", "settings", "sing", "something", "spelling", "spring",
    "string", "testing", "thing", "warning", "wing", "wiring",
    "typing", "sharding", "streaming", "threading", "tooling", "modeling",
    "modelling", "heading", "headings", "wording", "docstring",
    "coding", "missing", "naming", "existing", "following", "building",
}

IZE_STEMS = (
    "author", "categor", "custom", "initial", "maxim", "memo", "minim",
    "normal", "optim", "organ", "priorit", "recogn", "sanit", "serial",
    "standard", "summar", "synchron", "util", "visual",
)
IZE_ENDINGS = ("e", "es", "ed", "ing", "ation", "ations", "er", "ers")
OUR_STEMS = ("behavi", "col", "fav", "flav", "hon", "lab", "neighb")
OUR_ENDINGS = ("", "s", "ed", "ing", "al")
OTHER_SPELLINGS = (
    ("analyze", "analyse"), ("analyzed", "analysed"),
    ("analyzing", "analysing"), ("analyzer", "analyser"),
    ("canceled", "cancelled"), ("canceling", "cancelling"),
    ("catalog", "catalogue"), ("center", "centre"), ("centered", "centred"),
    ("defense", "defence"), ("fulfill", "fulfil"), ("gray", "grey"),
    ("labeled", "labelled"), ("labeling", "labelling"),
    ("modeled", "modelled"), ("modeling", "modelling"),
    ("signaled", "signalled"), ("signaling", "signalling"),
    ("traveled", "travelled"),
)
AMERICAN_TO_BRITISH = dict(
    [(f"{s}iz{e}", f"{s}is{e}") for s in IZE_STEMS for e in IZE_ENDINGS]
    + [(f"{s}or{e}", f"{s}our{e}") for s in OUR_STEMS for e in OUR_ENDINGS]
    + list(OTHER_SPELLINGS)
)

CONTRACTIONS = re.compile(
    r"\b(\w+n't|i'm|i'd|i'll|i've|it's|that's|there's|here's|what's|let's|"
    r"you're|we're|they're|you'll|we'll|it'll|they'll|you've|we've|they've|"
    r"who's|isn't|aren't|can't|won't|don't)\b",
    re.IGNORECASE,
)

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(\w+ed|"
    r"made|done|given|shown|known|written|read|built|kept|held|taken|"
    r"found|left|put|set|split|hidden|broken|chosen|driven)\b",
    re.IGNORECASE,
)

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
BLOCK_START = re.compile(r"[ \t]*(?:[-*]|\d+\.|\||#+)[ \t]")
TABLE_RULE = re.compile(r"[ \t]*\|[-:| \t]+\|[ \t]*")


def strip_noise(text):
    """Remove code, URLs, and paths so they do not produce false reports."""
    text = re.sub(
        r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL
    )
    text = re.sub(r"`[^`\n]*`", " CODE ", text)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"\S+/\S+\.\w+", " PATH ", text)
    return text


def clean_line(line):
    if TABLE_RULE.fullmatch(line):
        return ""
    line = re.sub(r"^[ \t]*\|", "", line)
    line = re.sub(r"[ \t]*\|[ \t]*", ". ", line)
    line = re.sub(r"\*\*|__", "", line)
    line = re.sub(r"^[ \t]*(?:#+|[-*]|\d+\.)[ \t]+", "", line)
    return line.strip()


def paragraphs(text):
    para = []
    for no, raw in enumerate(text.split("\n"), 1):
        line = clean_line(raw)
        if para and (not line or BLOCK_START.match(raw)):
            yield para
            para = []
        if line:
            para.append((no, line))
    if para:
        yield para


def sentences(para):
    starts, joined = [], ""
    for _, line in para:
        starts.append(len(joined))
        joined += line + " "
    pos = 0
    for m in re.finditer(r"(?<=[.!?])\s+|$", joined):
        s = joined[pos : m.start()].strip()
        if s:
            yield para[bisect.bisect_right(starts, pos) - 1][0], s
        pos = m.end()


def lemma(word):
    w = word.lower().strip("'-")
    if w in UNAPPROVED:
        return w
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            base = w[: -len(suffix)]
            candidates = [base, base + "e"]
            if base[-1] == base[-2]:
                candidates.append(base[:-1])
            for candidate in candidates:
                if candidate in UNAPPROVED:
                    return candidate
    return w


def check(text, source, allowed, spelling):
    errors, warns = [], []
    for para in paragraphs(strip_noise(text)):
        sents = list(sentences(para))
        if len(sents) > 6:
            warns.append((source, para[0][0], f"paragraph has {len(sents)} sentences (limit 6)"))
        for line_no, s in sents:
            words = WORD.findall(s)
            n = len(words)
            preview = s[:70]
            if ";" in s:
                errors.append((source, line_no, f"semicolon: '{preview}'"))
            if "—" in s:
                errors.append((source, line_no, f"em dash: '{preview}'"))
            for m in CONTRACTIONS.finditer(s):
                errors.append((source, line_no, f"contraction '{m.group(0)}': '{preview}'"))
            if n > 25:
                errors.append((source, line_no, f"{n} words (limit 25): '{preview}'"))
            elif n > 20:
                warns.append((source, line_no, f"{n} words (limit 20 for an instruction): '{preview}'"))
            for w in words:
                lw = w.lower()
                base = lemma(w)
                if lw in allowed or base in allowed:
                    continue
                if base in UNAPPROVED:
                    errors.append((source, line_no, f"unapproved '{w}' -> {UNAPPROVED[base]}: '{preview}'"))
                elif lw in spelling:
                    errors.append((source, line_no, f"spelling '{w}' -> {spelling[lw]}: '{preview}'"))
                elif lw.endswith("ing") and lw not in TECHNICAL_ING_WORDS and len(w) > 5:
                    warns.append((source, line_no, f"'-ing' form '{w}' (3.5): '{preview}'"))
            for m in PASSIVE.finditer(s):
                warns.append((source, line_no, f"possible passive '{m.group(0)}': '{preview}'"))
    return errors, warns


def load_allowed(args):
    words = set()
    for item in args.allow:
        words.update(item.split(","))
    for path in args.allow_file:
        with open(path, encoding="utf-8") as f:
            words.update(re.split(r"[\s,]+", f.read()))
    return {w.strip().lower() for w in words if w.strip()}


def main(argv):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("files", nargs="+", metavar="FILE", help="file to check, or - for stdin")
    parser.add_argument(
        "--spelling", choices=("american", "british"), default="american",
        help="spelling to enforce (default: american)",
    )
    parser.add_argument(
        "--allow", action="append", default=[], metavar="WORD,WORD",
        help="permit these technical names (repeatable)",
    )
    parser.add_argument(
        "--allow-file", action="append", default=[], metavar="PATH",
        help="permit the words in this file, separated by whitespace or commas (repeatable)",
    )
    args = parser.parse_args(argv)
    allowed = load_allowed(args)
    if args.spelling == "british":
        spelling = AMERICAN_TO_BRITISH
    else:
        spelling = {b: a for a, b in AMERICAN_TO_BRITISH.items()}

    all_errors, all_warns = [], []
    for path in args.files:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        e, w = check(text, path, allowed, spelling)
        all_errors += e
        all_warns += w
    for src, line, msg in all_errors:
        print(f"ERROR {src}:{line}: {msg}")
    for src, line, msg in all_warns:
        print(f"WARN  {src}:{line}: {msg}")
    print(f"\n{len(all_errors)} error(s), {len(all_warns)} warning(s)")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
