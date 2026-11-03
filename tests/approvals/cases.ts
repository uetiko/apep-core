// Matriz mínima y genérica de regresión de approvals. Cada caso se RESUELVE con el
// resolutor del runtime instalado; ningún comando ni tool se ejecuta.
//
// expected:  ALLOW (sin diálogo) | PROMPT (pide aprobación) | DENY (bloqueada siempre).
// target:    tool registrada (`read`, `write`, `bash`, `eval`, `task`) o prelude de eval (`browser`).
// mode:      fuerza el approvalMode del caso; por defecto, el efectivo de la config.
// policies:  `without:<key>` resuelve con `tools.approval` efectivo menos esa clave.
//
// Estos casos describen el patrón de gates recomendado por Apep Core
// (docs/recommended-approval-patterns.md) y presuponen que el proyecto que ejecuta
// la suite declara ese patrón en su propio `.omp/config.yml`: lectura libre,
// destrucción local y escritura de historia/estado compartido con confirmación.

export type Expected = "ALLOW" | "PROMPT" | "DENY";

export interface ApprovalCase {
	id: string;
	group: string;
	target: { kind: "tool" | "prelude"; name: string };
	args: Record<string, unknown>;
	expected: Expected;
	mode?: "always-ask" | "write" | "yolo";
	policies?: { without: string };
	note?: string;
}

const bash = (id: string, group: string, command: string, expected: Expected, note?: string): ApprovalCase => ({
	id,
	group,
	target: { kind: "tool", name: "bash" },
	args: { command },
	expected,
	note,
});

export const CASES: ApprovalCase[] = [
	// ── Tools no-bash ───────────────────────────────────────────────────────
	{ id: "T01", group: "files", target: { kind: "tool", name: "read" }, args: { path: "README.md" }, expected: "ALLOW" },

	// ── Git: lectura libre ──────────────────────────────────────────────────
	bash("G01", "git-read", "git status", "ALLOW"),
	bash("G02", "git-read", "git diff", "ALLOW"),
	bash("G03", "git-read", "git log --oneline -20", "ALLOW"),

	// ── Git: escritura de historia o estado compartido ──────────────────────
	bash("G20", "git-material", "git commit -m 'feat: x'", "PROMPT"),
	bash("G21", "git-material", "git push origin feature/example", "PROMPT"),
	bash("G22", "git-material", "git rebase main", "PROMPT"),
	bash("G23", "git-material", "git reset --hard HEAD~1", "PROMPT"),
	bash("G24", "git-material", "git clean -fdx", "PROMPT"),

	// ── Filesystem destructivo ──────────────────────────────────────────────
	bash("D01", "fs-destructive", "rm -rf build", "PROMPT"),

	// ── Worktrees de ejecución ──────────────────────────────────────────────
	bash("W01", "exec-worktree", "git worktree add .worktrees/exec-ID-1 -b feature/ID-1/example main", "PROMPT", "crear el worktree crea la work branch: gate"),
	bash("W02", "exec-worktree", "git worktree add .worktrees/exec-ID-1 feature/ID-1/example", "PROMPT", "rama existente: también gate"),
	bash("W03", "exec-worktree", "git worktree remove .worktrees/exec-ID-1", "PROMPT", "limpieza: gate"),
	bash("W04", "exec-worktree", "git worktree remove --force .worktrees/exec-ID-1", "PROMPT", "nunca --force"),
	bash("W05", "exec-worktree", "git -C .worktrees/exec-ID-1 commit -m x", "PROMPT", "commit dentro del worktree sigue con gate"),
	bash("W06", "exec-worktree", "git -C .worktrees/exec-ID-1 push origin feature/ID-1/example", "PROMPT", "push dentro del worktree sigue con gate"),
	bash("W07", "exec-worktree", "git worktree list", "ALLOW", "observación"),
];
