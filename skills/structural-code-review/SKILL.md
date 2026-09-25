---
name: structural-code-review
description: >-
  Strict review of a code change for structure and design quality, and defects. Use for a code quality review, a design review, a maintainability
  review, or a code quality audit of a branch, pull request, or diff. Reports
  only Critical, High, and Medium results. Writes the report in ASD-STE100.
disable-model-invocation: true
---

# Structural Code Review

Perform a deep and thorough audit of the code quality from a selected change. Find a different structure or implementation that makes the code much better and keeps the behavior the same. Make the abstractions and the modularity better. Delete spaghetti code. Make the code shorter and easier to read.

Be ambitious: before you accept the change as written, look for the structure that makes most of it unnecessary.
If a clear path to a better implementation needs a restructure of part of the codebase, recommend it.
The best result removes full branches, modes, helpers, or layers.
A result that moves the same complexity to a different file is not sufficient.

Be thorough and rigorous. Check each finding twice before you report it.

## 1. Select the code

- Examine the code that the user selects. If the user selects nothing, compare the branch with the merge base of the target branch, and include uncommitted changes.
- If you do not know the target branch, tell the user.
- Read the project instructions, build commands, and test commands.
- Read each changed file in full, and the callers and tests of each changed function. A diff alone hides structure.
- Read the applicable reference: [Rust](references/rust.md), [Android](references/android.md), [Terraform](references/terraform.md), [Puppet](references/puppet.md), or [TypeScript](references/typescript.md). For other languages, use the documents of the language for the project version.
- Report a defect from before the change only when the change increases its effect, or when the user wants a full audit.
- Do not change source files. Do not send the report to other persons.

## 2. Examine the design

Find the smaller set of concepts that gives the same behavior.
When a local change cannot remove the cause, recommend the different structure.

- Recommend deep modules: much behavior behind a small interface. Callers must not know internal decisions.
- Find a wrapper, adapter, or helper that adds no contract, isolation, or behavior. Recommend its removal. Keep a small adapter that protects a boundary or satisfies a framework contract.
- Find the same rule or state check in more than two locations. Recommend one owner for the rule and its data.
- Find a new condition, flag, or mode in a shared flow. This is a design defect, not a style problem. Recommend a state model, a type, or a policy object that removes the branches.
- Find feature logic in a shared path, or a helper that copies one the codebase already has. Recommend the canonical owner.
- Find a cast, an optional field, a nullable mode, or an `any` that hides an unclear invariant. Recommend a type that makes the invariant explicit.
- Find generic mechanisms, reflection, or string-typed dispatch that hides an easy data shape. Recommend the direct version.
- Find independent steps in sequence. Recommend parallel steps only when the parallel version is also clearer and has limits on work.
- Do not unite code that only looks the same. Two pieces that change for different causes are two pieces.
- Reject extension points, configuration modes, and generality that no requirement needs at this time.
- Examine machine-written code with the same standard as other code.

For a design result, show the rule that occurs again or the decision that callers know.
Show the cost at this time with code locations.
Give the owner and interface that you recommend.
Give the branches, concepts, or dependencies that the change removes.
Keep behavior and public contracts the same unless a defect makes a change necessary.

### File and function size

- Use 400 source lines as the point where you examine the structure of a file.
- Do not count blank lines, comments, machine-written files, lockfiles, or fixtures.
- Count tests apart from production code.
- A change that takes a file over 400 lines is a High result unless the author gives a structural cause.
- A change that takes a file over 800 lines is a Critical result unless the author divides the file first.
- A changed function over 60 lines, or with more than three levels of nesting, is a Medium result unless it stays flat and has one responsibility.

**Do not** divide a deep module only to decrease its line count.
For a size result, show the responsibilities that change for different causes.
Show the boundary that you recommend for the division.

## 3. Examine the behavior

Follow each changed path from input to output. Include failure paths and recovery paths.

- Check input validation, access control, and the protection of secrets.
- Check the data contract at each system boundary. Find invalid states that the code accepts.
- Check error paths for errors that the code does not return or record.
- Find fallback values and success results that hide a defect.
- Check resource ownership, cleanup, cancellation, retries, and limits on work.
- Check related writes for a state that stays half-applied after a failure. Recommend one transaction, or recovery when one transaction is not possible.
- Check concurrent operations for races, deadlocks, and incorrect sequence.
- Check compatibility, data migrations, and recovery after a release failure.
- Compare each API call and dependency with the version that the project uses.
- Compare the tests with the necessary behavior. Find assertions that pass when the behavior is incorrect.

Use the project checks that can show a defect.
Make a small reproduction when a result needs one.
Do not run commands that change a production system.

## 4. Keep only necessary results

Keep a result only when all of these are true:

- The result is about the selected code.
- The code, or a check that you ran, shows that the result is correct.
- A specified condition causes a defect or a large cost to change.
- The correction removes or decreases that cause.
- The result is Medium or above.

Put results with the same cause together. Keep them apart when the corrections are different.
Do not report format, names, or performance without a related defect or measure.
Do not add results to get a specified number of results.
Do not use Medium for a small problem only to include it.
If information is missing, tell the user in Limits what is necessary to complete the review.

| Level | Effect |
| --- | --- |
| 🔴 Critical | A path to system compromise, service failure for many users, or data loss without recovery. Also a structural regression that each subsequent change pays for. Examples: a change that takes a file over 800 lines, a new mode in a shared flow, a missed structure that removes most of the change. Correct before anything else. |
| 🟠 High | A path to incorrect important behavior, or a security control that does not operate. Also a structural cost that the author must correct or justify before merge. Examples: a shallow wrapper, a copy of a canonical helper, a hidden invariant, a file over 400 lines. |
| 🟡 Medium | A defect with a small effect. Also a design cost that the author corrects in this change or records as a task. Examples: a long function, the same check in three places, a test that reads internal state. |

Select the level from the effect and the number of users or systems it touches.
Use High or Critical for a design result only when the code shows the effect.

## 5. Write the report

Write all report text in ASD-STE100. Obey [report language](references/report-language.md).
Run `python3 <this skill's directory>/scripts/check_review_language.py <draft>` and correct each error.
Do not change code identifiers, paths, commands, or quoted output.

Write about the code and its effect. Do not write about the author.
Give the condition, the behavior, and the effect. Then give the correction and its cause.
For a defect, give the correction as an instruction.
For a design selection, give the alternatives, and end with the one that you recommend.

When the author knows something that you do not, end the result with a sentence that the author must answer.

Put results in this sequence: Critical, High, Medium. Do not add an empty level.
Use this structure for each result:

```text
### 🟠 High: <the effect in a few words>
Location: <path:line or a small range>

<Condition, behavior, and effect.>
<Correction, and what the code loses or gains.>
Check: <the test or inspection that shows the correction is correct.>
```

Keep one cause for each result. Use short paragraphs. Quote only the code that the result needs.

End the report with one line for Checks: the checks that you ran and their results.
Add Limits only for missing access, code that you did not examine, or assumptions that you made.
If there are no results, write this sentence:

`The review found no Critical, High, or Medium results in the selected code.`
Do not approve when the review is not complete.
