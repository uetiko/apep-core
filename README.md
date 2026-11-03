# Apep Core

Apep Core is a reusable, organization-independent engineering harness for OMP: methodology, skills, agents, commands and rules for specification, delivery, review and diagnostics.

Design invariant: `REMOVE DINAMIC → APEP CORE REMAINS A VALID ENGINEERING HARNESS`.

## Contents

- **Skills (11):** `project-management`, `technical-discovery`, `diagnostics`, `code-quality`, `implementation-review`, `security-review`, `architecture-review`, `delivery-lifecycle`, `specification`, `git-workflow`, `pr-review`.
- **Agents (6):** `delivery-orchestrator`, `implementation`, `diagnostics`, `governance-review`, `technical-discovery`, `architecture-review`.
- **Commands (9):** `project`, `shape`, `review`, `deliver`, `spec`, `design`, `diagnose`, `discover`, `pr`.
- **Rules (1):** `engineering-discipline` (`alwaysApply: true`).
- **Docs:** `docs/governance/ENGINEERING_GOVERNANCE.md`, `docs/recommended-approval-patterns.md`, `docs/agents-md-template.md`.
- **Tooling:** `ebook/` (EPUB build/validation), `tests/` (behavioral suites).

`pr-review` and `git-workflow` are provider-agnostic: concrete remote mechanics (e.g. a specific PR provider) and organization-specific branching conventions come from a separate organization plugin.

## What is NOT shipped

OMP plugins cannot contribute settings (`config.yml`, `bash.patterns`, approval policy) or always-loaded context files (`AGENTS.md`). Apep Core therefore ships no functional equivalents of those. Instead:

- [docs/recommended-approval-patterns.md](docs/recommended-approval-patterns.md) — what to put in your own `config.yml`.
- [docs/agents-md-template.md](docs/agents-md-template.md) — a template for your own `.omp/AGENTS.md`.

## License

**CC BY 4.0** (Creative Commons Attribution 4.0 International) — see [LICENSE.md](LICENSE.md). Decided 2026-11-03: content/methodology (no executable code ships in this package), free to share and adapt, even commercially, with attribution.

## Local development

```
omp plugin link <path-to-apep>
```

## Repository

`git@github.com:uetiko/apep-core.git` (`https://github.com/uetiko/apep-core`) — personal GitHub of the maintainer, public. OSIRIS (this workspace) is where it is edited today; the repo is the publication point, not the source of truth yet.
