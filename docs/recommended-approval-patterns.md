# Recommended approval patterns

OMP approval policy (`tools.approvalMode`, `bash.patterns`) lives in each consuming project's own `.omp/config.yml`. A plugin cannot ship it, so Apep Core cannot enforce any of the patterns below. This document is advisory: it describes a reusable pattern for you to adapt.

## Principles

- `THE HARNESS GOVERNS INTENT`: the approval layer classifies what a command is *for* (read, local change, publish), not just its binary name.
- `POLICY_PERMITS != TOOL_LAYER_AUTO_APPROVES`: a skill or rule saying an operation is allowed does not mean the tool layer will skip confirmation. If the runtime asks, report it and continue once approved; never look for a less observable route around the prompt.

## Gate tiers for VCS commands

| Tier | Examples | Suggested policy |
|---|---|---|
| Read-only | `status`, `log`, `diff`, `show`, `branch --list`, `blame` | allow |
| Local-destructive | `reset --hard`, `clean`, `checkout -- <path>`, `restore`, `stash drop`, `branch -D` | confirm |
| Publish / history-rewrite | `commit`, `push`, `push --force`, `rebase`, `merge`, `tag`, `cherry-pick`, `revert`, `commit --amend` | confirm |

## Ordering: first match wins

`bash.patterns` are evaluated in order and the first matching pattern decides. Consequence: specific `confirm`/`deny` patterns must come **before** broad catch-all `allow` patterns. A catch-all `allow` placed first silently shadows every stricter rule below it. Put catch-alls last.

## Cloud and platform CLIs

Default any cloud-provider or remote-platform CLI to confirmation-required. Allow only clearly read-only/introspection calls (e.g. `get-*`, `list-*`, `describe-*` style verbs), and keep mutating verbs (`create`, `update`, `delete`, `put`, `merge`, `approve`, `send`) gated.

Si tu organización usa un proveedor cloud o de control de versiones específico, añade sus patrones concretos a tu propio `config.yml`; este documento no los define por ti.
