---
name: structural-code-review
description: >-
  Strict review of a code change for structure and design quality. Use for a
  code quality review, a design review, a maintainability review, or a code
  quality audit of a branch, pull request, or diff. Reports only Critical,
  High, and Medium results. Writes the report in ASD-STE100.
disable-model-invocation: true
---

# Structural Code Review

Perform a deep and thorough audit of the code quality from a selected change. Find a different structure or implementation that makes the code much better and keeps the behavior the same. Make the abstractions and the modularity better. Delete spaghetti code. Make the code shorter and easier to read.

## Guiding Principles

- Be ambitious: before you accept the change as written, look for the structure that makes most of it unnecessary.
- If a clear path to a better implementation needs a restructure of part of the codebase, recommend it.
- The best result removes full branches, modes, helpers, or layers.
- A result that moves the same complexity to a different file is not sufficient.
- Correct behavior does not excuse a structural cost. A change that passes its tests and makes the code harder to change is a result.

**Be thorough and be rigorous.**

## 1. Select the code

- Examine the code that the user selects. If the user selects nothing, compare the branch with the merge base of the target branch, and include uncommitted changes.
- If you do not know the target branch, tell the user.
- Read the project instructions, build commands, and test commands.
- Read each changed file in full, and the callers and tests of each changed function. A diff alone hides structure.
- Read the applicable reference: [Rust](references/rust.md), [Android](references/android.md), [Terraform](references/terraform.md), [Puppet](references/puppet.md), or [TypeScript](references/typescript.md). For other languages, use the documents of the language for the project version.
- Report a problem from before the change only when the change makes it worse, or when the user wants a full audit.
- Use the project build, type check, and lint to confirm the facts that a result depends on. Do not run commands that change a production system.
- Do not change source files. Do not send the report to other persons.

## 2. Examine the design

Your main job is to find the design that makes most of this change unnecessary.
Kent Beck puts it as "make the change easy, then make the easy change". Look for the restructure that would have made this change small.

Ask these questions about each meaningful part of the change:

- Is there a restructure that would turn this change into a small one?
- Could an existing abstraction absorb this with a small extension?
- Would a different state model or data shape make these branches disappear?
- Could the special case become the default flow, so that no exception is necessary?
- Does this refactor delete concepts, or only move them to a different place?

When a local change cannot remove the cause, recommend the different structure.
The rules below are common forms of the problem, not a full list.

- Find a module, class, or function with an interface that is almost as complex as its body. Recommend a deeper interface that hides the decision from callers.
- Find a change that makes an existing interface wider: a new parameter, flag, export, or exception that callers must know. Recommend that the module absorbs the decision.
- Find a wrapper, adapter, pass-through method, or pass-through variable that adds no contract, isolation, or behavior. Recommend its removal.
- Find a refactor that moves concepts to a new place but does not remove them. Recommend a structure with fewer concepts, or the removal of the refactor. Count the concepts, not the files.
- Find one design decision that two or more modules know: a rule, a format, a state check, or a sequence. Recommend one owner for the decision and its data. Count the same knowledge, not the same text.
- Find code divided by the sequence of steps, where each step knows the same decision. Recommend a division by knowledge.
- Find a new condition, flag, or mode in a shared flow. This is a design defect, not a style problem. Recommend a state model, a type, or a policy object that removes the branches.
- Find feature logic in a shared path, or a helper that copies one the codebase already has. Recommend the canonical owner.
- Find a cast, an optional field, a nullable mode, an `any`, or a silent fallback that hides an unclear invariant. Recommend a type that makes the invariant explicit.
- Find generic mechanisms, reflection, or string-typed dispatch that hides an easy data shape. Recommend the direct version.
- Find an interface shaped around the special case of one caller. Recommend a somewhat general-purpose interface when it is simpler for all callers.
- Find extension points and configuration modes that no caller uses. Recommend their removal.
- Find independent steps in sequence where the parallel version is clearer. Recommend the parallel version.
- Find related updates that can leave state half-applied after a failure. Recommend one transaction, or one owner for the update.
- Examine machine-written code with the same standard as other code.

Report a match even when you think an exception applies. The author must give the cause for the exception.

For a design result, show the rule that occurs again or the decision that callers know.
Show the cost at this time with code locations.
Give the owner and interface that you recommend.
Give the branches, concepts, or dependencies that the change removes.
Keep behavior and public contracts the same.

### File and function size

- Use 400 source lines as the point where you examine the structure of a file.
- Do not count blank lines, comments, machine-written files, lockfiles, or fixtures.
- Count tests apart from production code.
- A change that takes a file over 400 lines is a High result unless the author gives a structural cause.
- A change that takes a file over 800 lines is a Critical result unless the author divides the file first.
- Use 60 lines as the point where you examine the structure of a changed function. A changed function that mixes responsibilities, or has more than three levels of nesting, is a Medium result.

For a size result, show the responsibilities that change for different causes.
Show the boundary that you recommend for the division.

## 3. Keep only necessary results

Keep a result only when all of these are true:

- The result is about the selected code.
- The code, or a check that you ran, shows that the result is correct.
- The structure causes a large cost to change the code.
- The correction removes or decreases that cause.
- The result is Medium or above.

These tests are strict for small results. For a structural result, the evidence is the smaller design: its shape, and the branches and concepts that it removes.
Do not remove a structural result only because a build or a test cannot prove it.

Put results with the same cause together. Keep them apart when the corrections are different.
Do not report format or performance. Report a name only when it hides a design problem.
Do not add results to get a specified number of results.
Do not use Medium for a small problem only to include it.
If information is missing, tell the user in Limits what is necessary to complete the review.

| Level | Effect |
| --- | --- |
| 🔴 Critical | A structural regression that each subsequent change pays for. Examples: a change that takes a file over 800 lines, a new mode in a shared flow, a missed structure that removes most of the change. Correct before anything else. |
| 🟠 High | A structural cost that the author must correct or justify before merge. Examples: a shallow wrapper, a copy of a canonical helper, a hidden invariant, a file over 400 lines. |
| 🟡 Medium | A design cost that the author corrects in this change or records as a task. Examples: a function that mixes responsibilities, the same check in three places, a test that reads internal state. |

Select the level from the cost: how many subsequent changes pay for it, and how many modules it touches.
Use High or Critical only when the code shows the cost. For a structural result, the sketch shows what the correction removes.

## 4. Write the report

Write all report text in ASD-STE100. Obey [report language](references/report-language.md).
Run `python3 <this skill's directory>/scripts/check_review_language.py <draft>` and correct each error.
Do not change code identifiers, paths, commands, or quoted output.

Write about the code and its effect. Do not write about the author.
Give the condition, the behavior, and the effect. Then give the correction and its cause.
When one correction is clear, give it as an instruction.
When there are alternatives, give them, and end with the one that you recommend.

When the author knows something that you do not, end the result with a sentence that the author must answer.

Put results in this sequence: Critical, High, Medium. Do not add an empty level.
Use this structure for each result:

```text
### 1. 🟠 High: <the effect in a few words>

📍 Location: <path:line or a small range>

<Condition, behavior, and effect.>
<Correction, and what the code loses or gains.>
📝 Sketch: <for a structural result only: the types, signatures, or call site after the correction.>
🧪 Check: <the test or inspection that shows the correction keeps the behavior.>
```

Keep one cause for each result. Use short paragraphs. Quote only the code that the result needs. Keep a sketch to the lines that show the new shape.

Before Checks, add one line for Smaller design: the design that you recommend, or the designs that you examined and the cause that each one is not simpler.
End the report with one line for Checks: the checks that you ran and their results.
Add Limits only for missing access, code that you did not examine, or assumptions that you made.
If there are no results, write this sentence:

`The review found no Critical, High, or Medium results in the selected code.`
