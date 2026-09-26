---
name: init-brownserve-project-skills
description: "Write the per-repo config (`.agents/project.json`) that the Brownserve project skills read to know where issues and design documents go. Run once per repo, and again to check or update it."
disable-model-invocation: true
---

# Init Brownserve Project Skills

Write `.agents/project.json`: the config that the Brownserve project skills read to know where issues and design documents go.
The skills do not work without this file, and they never guess its values. This skill is the only thing that writes it.

Work out every value yourself. Present the result and ask the user to confirm. Ask the user for a value only when exploration cannot settle it.

## The config

```json
{
  "version": 1,
  "project": "some-project",
  "issues": {
    "repo": "Brownserve-UK/some-project-core",
    "default_labels": ["server"]
  },
  "docs": {
    "repo": "Brownserve-UK/design_documents"
  }
}
```

| Field | Meaning |
| --- | --- |
| `version` | Config format version. Always `1`. |
| `project` | The slug used in design document filenames (`YYYY-MM-DD-<project>.md`). In a multi-repo project, this is the product name, not the repo name. |
| `issues.repo` | `owner/name` of the repo that holds issues for this repo. |
| `issues.default_labels` | Labels to apply to every issue raised from this repo. An empty array is valid. |
| `docs.repo` | `owner/name` of the central design documents repo. |

Every field is required. Write `default_labels: []` explicitly for a repo that needs none.

The design documents repos are cloned in the devcontainer at:

| Repo | Local path |
| --- | --- |
| `Brownserve-UK/design_documents_public` | `/home/bsdev/Repositories/design_documents_public` |
| `Brownserve-UK/design_documents` (private) | `/home/bsdev/Repositories/design_documents` |

`docs.repo` must be one of these two.

## Process

### 1. Explore

- `git remote -v`: the owner and name of this repo.
- `gh repo view <this repo> --json name,owner,visibility,hasIssuesEnabled`.
- `.agents/project.json`: does a config already exist? If so, read it.
- `git check-ignore -q .agents/project.json`: is the config path gitignored?

### 2. Classify the repo

| Signals | Kind | `issues.repo` | `docs.repo` | `project` |
| --- | --- | --- | --- | --- |
| Public, issues enabled | Standard | this repo | `design_documents_public` | repo name |
| Private, issues disabled, `<repo>-issues` exists | Closed source | `<repo>-issues` | `design_documents` | repo name |
| Issues disabled, a sibling with a shared name prefix has issues enabled | Multi-repo | that sibling | public or private, to match this repo's visibility | the shared prefix |

To find multi-repo siblings, list the owner's repos (`gh repo list <owner> --limit 1000 --json name,visibility,hasIssuesEnabled`) and keep those that share this repo's name prefix.

If the signals match no row, or match more than one, or more than one sibling has issues enabled, stop and ask the user. Do not pick.

### 3. Choose the default labels

Get the labels that exist in `issues.repo` with `gh label list --repo <issues.repo> --limit 1000`.
Labels are managed by Terraform. Choose only from labels that already exist. Never create a label.

- Standard and closed source: propose `[]`.
- Multi-repo: propose the label that matches this repo's part of the name (`some-project-server` → `server`). If no such label exists, stop and tell the user it must be added in Terraform first.

### 4. Validate

Every check is a hard failure. Stop and report the cause. There is no override.

- `issues.repo` exists, is not archived, and has issues enabled.
- Every entry in `default_labels` exists in `issues.repo`.
- If this repo is private, `issues.repo` is private.
- If this repo is private, `docs.repo` is `design_documents` (private).
- `docs.repo` exists (check with `gh repo view`). Do not require the local clone. It can be missing from this container.

### 5. Confirm

Show the user the proposed config and how each value was worked out.
If a config already exists, show a diff against it. If nothing has changed, say so and stop.
Write nothing until the user confirms.

### 6. Write

Write `.agents/project.json` with two-space indentation and a trailing newline.

If step 1 found the path is gitignored, tell the user that the config will not be committed until the gitignore tool allows `.agents/project.json`. Do not edit `.gitignore`: it is generated.
