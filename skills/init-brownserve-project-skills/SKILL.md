---
name: init-brownserve-project-skills
description: "Write the per-repo config (`.agents/project.json`) that the Brownserve project skills read to know where issues and design documents go. Run once per repo, and again to check or update it."
disable-model-invocation: true
---

# Init Brownserve Project Skills

Write `.agents/project.json`: the config that the Brownserve project skills read to know where issues and design documents go.
The skills do not work without this file, and they never guess its values. This skill is the only thing that writes it.

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
| `project` | The name of the product/project. Necessary as the it may differ from the repo name. |
| `issues.repo` | `owner/repo` of the repo that holds issues for this repo. |
| `issues.default_labels` | Labels to apply to every issue raised from this repo. An empty array is valid. |
| `docs.repo` | `owner/repo` of the central design documents repo. |

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
- `gh repo view <this repo> --json visibility`: is this repo private?
- `.agents/project.json`: does a config already exist? If so, read it.
- `git check-ignore -q .agents/project.json`: is the config path gitignored?

### 2. Ask the kind of repo

If the invocation text states the kind, use it and do not ask. Otherwise, ask the user which kind of repo this is: standard, closed source, or multi-repo. Do not suggest one.

### 3. Get the values

| Kind | `issues.repo` | `default_labels` | `docs.repo` | `project` |
| --- | --- | --- | --- | --- |
| Standard | this repo | `[]` | `design_documents_public` | repo name |
| Closed source | `<repo>-issues` | `[]` | `design_documents` | repo name |
| Multi-repo | ask | ask | `design_documents` if this repo is private, else `design_documents_public` | ask |

For a multi-repo project, ask for each value in turn. Skip a value that the invocation text already gives.

1. The issue repo. It can be this repo.
2. The project name.
3. The default labels. Get the labels that exist in the issue repo with `gh label list --repo <issues.repo> --limit 1000`, and ask the user to choose from them.

Labels are managed by Terraform. Never create a label. If a label the user wants does not exist, stop and tell them it must be added in Terraform first.

### 4. Validate

Every check is a hard failure. Stop and report the cause. There is no override.

- `issues.repo` exists, is not archived, and has issues enabled.
- Every entry in `default_labels` exists in `issues.repo`.
- If this repo is private, `issues.repo` is private.
- If this repo is private, `docs.repo` is `design_documents` (private).
- `docs.repo` exists (check with `gh repo view`). Do not require the local clone. It can be missing from this container.

### 5. Confirm

Show the user the proposed config.
If a config already exists, show a diff against it. If nothing has changed, say so and stop.
Write nothing until the user confirms.

### 6. Write

Write `.agents/project.json` with two-space indentation and a trailing newline.

If step 1 found the path is gitignored, tell the user that the config will not be committed until the gitignore tool allows `.agents/project.json`. Do not edit `.gitignore`: it is generated.
