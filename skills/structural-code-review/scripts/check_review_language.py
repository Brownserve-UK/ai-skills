#!/usr/bin/env python3
"""Check review text against the ASD-STE100 rules that a script can test.

Usage:
    python3 check_review_language.py REVIEW.md [MORE.md ...]
    cat REVIEW.md | python3 check_review_language.py -

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
    WARN   sentence with 21 to 25 words (limit 20 for instructions)
    WARN   "-ing" word that is not a known technical name (3.5)
    WARN   possible passive voice                         (3.6)
    WARN   paragraph with more than six sentences         (6.6)

The word table is small. It holds the words that appear most often in code
reviews and that the STE dictionary does not approve. The full dictionary is
in the standard itself. Add technical names of your codebase to
TECHNICAL_ING_WORDS when the script reports them.
"""

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
    "avoid": "prevent",
    "choice": "selection",
    "combine": "mix, or put together",
    "complex": "not easy",
    "complicated": "not easy",
    "consider": "think about",
    "could": "can",
    "cross": "go across",
    "delete": "remove, erase",
    "detail": "instruction, or give",
    "ensure": "make sure",
    "exact": "accurate",
    "expect": "think, or possible",
    "explain": "tell, or give the cause",
    "fail": "does not",
    "grow": "become",
    "however": "but",
    "implement": "do, make",
    "improve": "make better",
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
    "reduce": "decrease",
    "require": "must, necessary",
    "serious": "important",
    "several": "some",
    "severe": "dangerous",
    "should": "must",
    "simple": "easy",
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
    "routing", "setting", "settings", "sing", "something", "spring",
    "string", "testing", "thing", "warning", "wing", "wiring", "string",
    "typing", "sharding", "streaming", "threading", "tooling", "modeling",
    "finding", "findings", "heading", "headings", "wording", "docstring",
    "coding", "missing", "naming", "existing", "following", "building",
}

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


def strip_noise(text):
    """Remove code, URLs, and paths so they do not produce false reports."""
    text = re.sub(r"```.*?```", "\n", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", " CODE ", text)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"\S+/\S+\.\w+", " PATH ", text)
    text = re.sub(r"^\|[-:| ]+\|\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n(?=[ \t]*(?:[-*]|\d+\.|\|)[ \t])", "\n\n", text)
    text = re.sub(r"^\|", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]*\|[ \t]*", ". ", text)
    text = re.sub(r"\*\*|__|^#+[ \t]*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]*[-*][ \t]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]*\d+\.[ \t]+", "", text, flags=re.MULTILINE)
    return text


def sentences(paragraph):
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p for p in parts if p]


def lemma(word):
    w = word.lower().strip("'-")
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            base = w[: -len(suffix)]
            if base in UNAPPROVED:
                return base
            if suffix == "ing" and base + "e" in UNAPPROVED:
                return base + "e"
    return w


def check(text, source):
    errors, warns = [], []
    clean = strip_noise(text)
    paragraphs = re.split(r"\n\s*\n", clean)
    line_no = 1
    for para in paragraphs:
        sents = sentences(para)
        if len(sents) > 6:
            warns.append((source, line_no, f"paragraph has {len(sents)} sentences (limit 6)"))
        for s in sents:
            words = WORD.findall(s)
            n = len(words)
            preview = s[:70].replace("\n", " ")
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
                base = lemma(w)
                if base in UNAPPROVED:
                    errors.append((source, line_no, f"unapproved '{w}' -> {UNAPPROVED[base]}: '{preview}'"))
                elif w.lower().endswith("ing") and w.lower() not in TECHNICAL_ING_WORDS and len(w) > 5:
                    warns.append((source, line_no, f"'-ing' form '{w}' (3.5): '{preview}'"))
            for m in PASSIVE.finditer(s):
                warns.append((source, line_no, f"possible passive '{m.group(0)}': '{preview}'"))
        line_no += para.count("\n") + 2
    return errors, warns


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    all_errors, all_warns = [], []
    for path in argv:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        e, w = check(text, path)
        all_errors += e
        all_warns += w
    for src, line, msg in all_errors:
        print(f"ERROR {src}:~{line}: {msg}")
    for src, line, msg in all_warns:
        print(f"WARN  {src}:~{line}: {msg}")
    print(f"\n{len(all_errors)} error(s), {len(all_warns)} warning(s)")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
