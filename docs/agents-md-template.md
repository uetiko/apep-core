# AGENTS.md template

OMP plugins cannot ship an auto-loaded `AGENTS.md` (always-loaded project background is a native, project-root file). A project that wants Apep Core's recommended workspace-context conventions should write its own `.omp/AGENTS.md`. The template below is generic; replace every `<placeholder>`.

## Session root

For a multi-repo workspace, start the OMP session from the directory that holds the governing `.omp/`. OMP's context/rules discovery walks up to the nearest non-empty `.omp/`, but settings discovery does not walk up at all — starting inside a subrepo silently loses project settings (`config.yml`, approval patterns).

## Template

```markdown
# <Workspace name> — workspace context

## 1. Governance precedence

workspace governance (`<path to ENGINEERING_GOVERNANCE.md equivalent>`)
  → repository governance (`<repo>/AGENTS.md` or `<repo>/IA.md`, when the repo has one)
  → task contract
  → implementation

A lower level never overrides a higher one. Silence is not authorization.

## 2. Progressive disclosure

Load only what the current task needs: skills on demand, references on demand,
repository-local governance only for the repository being touched.

## 3. Repository entry protocol

Before working in a repository:
1. Identify which repository the task targets.
2. Do not assume workspace-level git state applies to it; each repository has its own branch, HEAD and status.
3. Check whether the repository designates a local-authority file; if so, read it completely first.
4. Establish a per-repository baseline (branch, HEAD, `git status`, relevant pre-existing changes).

### Repositories with a designated local-authority file

| Repository | Authority file |
|---|---|
| `<repo-a>` | `<repo-a>/<file>` |
| (none declared) | — |
```
