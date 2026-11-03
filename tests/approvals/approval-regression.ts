// Extensión OMP de un solo uso: resuelve la matriz de `cases.ts` con el resolutor
// de approvals del runtime instalado y la config efectiva de la sesión, imprime el
// informe y termina el proceso en `session_start`, antes de cualquier turno del
// modelo. No ejecuta ningún comando ni tool. Lánzala con `run.sh`.
import {
	BashTool,
	EvalTool,
	ReadTool,
	settings,
	TaskTool,
	WriteTool,
} from "@oh-my-pi/pi-coding-agent";
import { resolveApproval } from "@oh-my-pi/pi-coding-agent/tools/approval";
import { createBrowserPreludeDefinition } from "@oh-my-pi/pi-coding-agent/tools/browser/prelude-definition";
import { type ApprovalCase, CASES, type Expected } from "./cases";

type Observed = Expected | "ERROR";

interface Row {
	c: ApprovalCase;
	observed: Observed;
	evidence: string;
}

const CONFIG_KEYS = ["tools.approvalMode", "tools.approval", "bash.allowCompoundCommands", "bash.patterns"] as const;

function buildTools(cwd: string): Record<string, any> {
	const session = { settings, cwd, enableLsp: false };
	const tools = [new ReadTool(session), new WriteTool(session), new BashTool(session), new EvalTool(session), new TaskTool(session, {})];
	return Object.fromEntries(tools.map(t => [t.name, t]));
}

function buildPreludes(cwd: string): Record<string, any> {
	const unused = () => {
		throw new Error("approval-regression: prelude invocation is not allowed");
	};
	const browser = createBrowserPreludeDefinition({ settings, cwd }, { invoke: unused, status: () => undefined });
	return { [browser.name]: browser };
}

function resolveCase(c: ApprovalCase, tools: Record<string, any>, preludes: Record<string, any>): Row {
	const mode = c.mode ?? settings.get("tools.approvalMode");
	const policies: Record<string, unknown> = { ...(settings.get("tools.approval") ?? {}) };
	if (c.policies) delete policies[c.policies.without];

	let subject: any;
	if (c.target.kind === "tool") {
		subject = tools[c.target.name];
	} else {
		// Mismo descriptor que construye `eval/preludes.ts` antes de resolver.
		const def = preludes[c.target.name];
		subject = def && { name: def.name, ...(def.approval !== undefined ? { approval: def.approval } : {}) };
	}
	if (!subject) return { c, observed: "ERROR", evidence: `${c.target.kind} "${c.target.name}" not found in runtime` };

	try {
		const d = resolveApproval(subject, c.args, mode, policies);
		const observed = d.policy.toUpperCase() as Expected;
		const parts = [`mode=${mode}`, `source=${d.source}`, `tier=${d.tier}`];
		if (d.override) parts.push("override");
		if (d.policyKey) parts.push(`key=${d.policyKey}`);
		if (d.reason) parts.push(`reason=${d.reason}`);
		return { c, observed, evidence: parts.join(" ") };
	} catch (e) {
		return { c, observed: "ERROR", evidence: String(e) };
	}
}

async function configEvidence(cwd: string): Promise<string[]> {
	const lines: string[] = [];
	const path = `${cwd}/.omp/config.yml`;
	const file = Bun.file(path);
	if (!(await file.exists())) return [`CONFIG_FILE: ${path} NOT FOUND — wrong session root`];
	const text = await file.text();
	const sha = new Bun.CryptoHasher("sha256").update(text).digest("hex");
	lines.push(`CONFIG_FILE: ${path}`, `CONFIG_SHA256: ${sha}`);

	const yaml = (Bun as any).YAML?.parse?.(text);
	for (const key of CONFIG_KEYS) {
		const effective = settings.get(key);
		const declared = yaml ? key.split(".").reduce((o: any, k) => o?.[k], yaml) : undefined;
		const same = yaml ? Bun.deepEquals(effective, declared) : undefined;
		const shown = key === "bash.patterns" ? `${(effective ?? []).length} rules` : JSON.stringify(effective);
		const verdict = same === undefined ? "file not parsed" : same ? "== config.yml" : "!= config.yml (overridden elsewhere)";
		lines.push(`EFFECTIVE ${key}: ${shown}  [${verdict}]`);
	}
	return lines;
}

function pad(s: string, n: number): string {
	return s.length >= n ? s : s + " ".repeat(n - s.length);
}

function render(rows: Row[]): string {
	const out: string[] = [];
	out.push(`${pad("CASE", 5)} ${pad("RESULT", 6)} ${pad("EXPECTED", 8)} ${pad("OBSERVED", 8)} ${pad("TARGET", 16)} INPUT  |  EVIDENCE`);
	for (const r of rows) {
		const result = r.observed === r.c.expected ? "PASS" : "FAIL";
		const input = r.c.target.name === "bash" ? String(r.c.args.command) : JSON.stringify(r.c.args);
		const target = `${r.c.target.kind}:${r.c.target.name}`;
		const note = r.c.note ? `  (${r.c.note})` : "";
		out.push(`${pad(r.c.id, 5)} ${pad(result, 6)} ${pad(r.c.expected, 8)} ${pad(r.observed, 8)} ${pad(target, 16)} ${input}${note}  |  ${r.evidence}`);
	}
	return out.join("\n");
}

export default function approvalRegression(pi: any) {
	// Defensa en profundidad: si el informe no hubiera terminado el proceso, nunca
	// se llega a enviar el prompt al modelo.
	pi.on("before_agent_start", () => {
		process.stderr.write("approval-regression: aborting before any model turn\n");
		process.exit(2);
	});

	pi.on("session_start", async (_event: any, ctx: any) => {
		let code = 2;
		try {
			const cwd: string = ctx.cwd;
			const tools = buildTools(cwd);
			const preludes = buildPreludes(cwd);
			const rows = CASES.map(c => resolveCase(c, tools, preludes));
			const fails = rows.filter(r => r.observed !== r.c.expected);

			const report = [
				"# OMP approval regression",
				`SESSION_ROOT: ${cwd}`,
				...(await configEvidence(cwd)),
				"EXECUTION: none — every case is resolved only (NOT_EXECUTED)",
				"",
				render(rows),
				"",
				`TOTAL: ${rows.length}  PASS: ${rows.length - fails.length}  FAIL: ${fails.length}`,
			].join("\n");
			process.stdout.write(`${report}\n`);
			const jsonOut = process.env.APPROVAL_REGRESSION_JSON;
			if (jsonOut) {
				await Bun.write(jsonOut, JSON.stringify(rows.map(r => ({ ...r.c, observed: r.observed, evidence: r.evidence })), null, 2));
			}
			code = fails.length === 0 ? 0 : 1;
		} catch (e) {
			process.stderr.write(`approval-regression: harness error: ${e instanceof Error ? e.stack : String(e)}\n`);
		} finally {
			process.exit(code);
		}
	});
}
