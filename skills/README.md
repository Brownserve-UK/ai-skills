# Skill overview

## [init-brownserve-project-skills](init-brownserve-project-skills/SKILL.md)

Writes `.agents/project.json`, the per-repo config that the project skills read to know where issues and design documents go.
Works out the values from GitHub and asks the user to confirm.

## [mock-up](mock-up/SKILL.md)

Allows for spinning up interactive design mock-ups and prototypes before writing code.
All served locally with live reload.
**Requires the `bsdev` container to run.**

## [plain-technical-english](plain-technical-english/SKILL.md)

Writing rules and a checker script for Plain Technical English, a relaxed form of ASD-STE100.
Used by other skills to keep their output short and hard to misread.
Can also be invoked directly to rewrite text.

## [structural-code-review](structural-code-review/SKILL.md)

Performs a review of code changes to try and reduce AI slop code.
Suggests changes ordered by severity.
Report is written in Plain Technical English, so **requires the `plain-technical-english` skill**.
Inspired by Cursor's [code review skill](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)