# Report language

Write the report in ASD-STE100 (Simplified Technical English).
STE removes two causes of incorrect reading: words with more than one meaning, and sentences with more than one structure.
A report in STE is short, direct, and hard to misread.
It also sounds fair, because STE has no room for sarcasm or vague hedges.

The controlling reference is ASD-STE100 Issue 8 (2021). Issue 9 (2025) has the same rules for this use.
Run `python3 <this skill's directory>/scripts/check_review_language.py <report>` on the report. Correct each error.
Do not treat a successful script run as proof of full compliance. The script tests only the rules that a script can test.

## Sentence rules

| Rule | Instruction |
| --- | --- |
| 1.1, 1.2 | Use approved words, and each word as one part of speech only. |
| 1.14 | Use American English spelling. |
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
The vocabulary of software is a set of technical names. Examples: module, interface, refactor, wrapper, cast, flag, enum, boundary, merge, pull request, author, caller, transaction, fallback.
Also the names in the codebase (types, functions, files), and the names of languages and tools.
Use them without change. Do not make new verbs from them (rule 1.7).
Do not call an ordinary unapproved word a technical name only to keep it.
Use each word with its usual meaning. Do not use metaphors, slang, or new words that you create.

These labels are fixed in the report: Critical, High, Medium, Location, Sketch, Check, Smaller design, Checks, Limits.
Keep identifiers, paths, commands, and quoted output unchanged. Use STE for the text around them.

## Words to replace

The script holds the full table. The most common replacements:

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

## Shape of a result

Give the condition, the behavior, and the effect first. Then give the correction and its cause.
Keep the strength of each claim. A conditional failure is not a failure that always occurs.
Give the correction directly. Do not use a polite phrase that makes the necessary action unclear.
When the author knows something that you do not, end with a sentence that the author must answer.

## Tone

Write as a senior colleague who wants the change to succeed.
Write about the code, not about the author. Give the cause with each recommendation.
Do not make a Critical result sound optional.

Use these sentences as patterns. Do not insert them without evidence in the code.

- "If the second write does not complete, the first write stays. The balance is then incorrect. Put both writes in one transaction."
- "The fallback returns success after the write does not complete. Return the error, so that the caller can retry."
- "Callers repeat the same state check in three places. Can one module own this rule?"
- "These wrappers give each caller access to the same storage fields. Move the conversion into the storage module, so that one contract exists."
- "Did you think about a `Sink` trait here? Then the five `if dry_run` branches become two implementations, and `plan()` does not change."
- "This does not do what the name says. When `retries` is 0, it returns before the first try."
- "I do not recommend a boolean parameter here. A second mode will come, and then this function has four paths."
- "Is there a caller that needs the old format and the new format at the same time? If not, the compatibility branch can go."
