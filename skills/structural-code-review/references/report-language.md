# Report language

These rules add to the `plain-technical-english` skill. They apply to the review report only.

## Fixed labels

These labels are fixed in the report: Critical, High, Medium, Location, Sketch, Check, Smaller design, Checks, Limits.

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
