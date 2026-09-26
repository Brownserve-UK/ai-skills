---
name: plain-technical-english
description: >-
  Rules and a checker for Plain Technical English (PTE), a relaxed form of
  ASD-STE100 for software text. Use only when a skill or the user tells you
  to write a named output in Plain Technical English or STE. Do not use it
  for other chat replies, code, or code comments.
---

# Plain Technical English

Plain Technical English (PTE) removes two causes of incorrect reading: words with more than one meaning, and sentences with more than one structure.
Text in PTE is short, direct, and hard to misread.
It also sounds fair, because PTE has no room for sarcasm or vague hedges.

## Scope

Apply these rules only to the output that the calling skill or the user names.
Other text in the session keeps its usual style. This includes code comments and other chat replies.
Keep code identifiers, paths, commands, and quoted output unchanged. Use PTE for the text around them.

A calling skill can give:

- The spelling: American (the default) or British.
- Technical names of its domain that the checker must not report.
- Labels and structure for its output. These rules apply to the text in that structure.

## Relation to ASD-STE100

PTE starts from ASD-STE100 Issue 8 (2021). This file, not the standard, is the primary reference.
Do not apply a rule or a dictionary entry from ASD-STE100 that this file does not contain.
These are the differences:

- Technical names: you can use the full vocabulary of software (a wider rule 1.5).
- Dictionary: the checker table holds the forbidden words. For other words, use the simplest word with one clear meaning. Do not replace a clear word only because the STE dictionary does not contain it.
- Spelling: the caller selects American or British English. Rule 1.14 lets you use only American English.
- Em dashes are forbidden (house style).

## Sentence rules

| Rule | Instruction |
| --- | --- |
| 1.1, 1.2 | Use approved words, and each word as one part of speech only. |
| 1.14 | Use the spelling that the caller selects. The default is American English. |
| 2.1 | Write noun clusters of three words or less. |
| 2.3 | Keep articles (the, a, an) and demonstrative adjectives (this, these). |
| 3.4 | Do not use `should`, `could`, `would`, `may`, `might`, or the perfect tenses. |
| 3.5 | Do not use the `-ing` form as a verb. |
| 3.6 | Use the active voice. Name the actor. |
| 4.2 | Do not use contractions. Do not remove words to make a sentence shorter. |
| 5.1, 6.3 | Sentences: 20 words or less for an instruction, 25 words or less for a description. |
| 5.2, 5.3 | One instruction in each sentence, in the imperative form. |
| 6.5, 6.6 | One topic in each paragraph. Six sentences or less in each paragraph. |
| 8.1 | Do not use the semicolon. Write two sentences. |
| 9.3 | Do not make phrasal verbs. "Remove", not `take out`. "Start", not `spin up`. |

## Technical names

Rule 1.5 lets the writer use the technical names of the field.
The vocabulary of software is a set of technical names. Examples: module, interface, refactor, wrapper, cast, flag, enum, boundary, merge, pull request, caller, transaction, fallback.
Also the names in the codebase (types, functions, files), and the names of languages and tools.
Use them without change. Do not make new verbs from them (rule 1.7).
Do not call an ordinary unapproved word a technical name only to keep it.
Use each word with its usual meaning. Do not use metaphors, slang, or new words that you create.

## Words to replace

The checker holds the full table. The most common replacements:

| Do not write | Write |
| --- | --- |
| `should`, `could`, `would`, `may`, `might` | must, can, will |
| `consider`, `suggest` | think about, recommend |
| `ensure`, `provide`, `require` | make sure, give, must |
| `reason`, `why` | cause, what is the cause |
| `however`, `therefore`, `instead` | but, as a result, as an alternative |
| `wrong`, `fail`, `consequence` | incorrect, does not, effect |
| `several`, `whole`, `amount` | some, full, quantity |
| `indicate`, `explain`, `understand` | show, tell, know |

## Meaning

Keep the strength of each claim. A conditional failure is not a failure that always occurs.
Give an instruction directly. Do not use a polite phrase that makes the necessary action unclear.

## Check the output

Write the output to a file, then run the checker on it:

```sh
python3 <this skill's directory>/scripts/check.py [--spelling british] [--allow WORD,WORD] [--allow-file PATH] <file>
```

Correct each ERROR. Examine each WARN, and correct it when it is a violation. Run the checker again until it shows no errors.

When the checker reports a technical name of the domain, add it with `--allow`. Do not use `--allow` to keep an ordinary word.
Do not treat a successful run as proof of full compliance. The checker tests only the rules that a script can test.
