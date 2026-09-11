---
name: init
description: Enable or check Veloci automatic task tracking in the actual execution environment.
---
# Enable automatic task tracking

Establish the actual execution host using the runtime's available tools and host identity. A mobile display is not an execution host. Do not guess from a user agent or assume Cowork/Work can read desktop files. If the execution host is unknown, ask where the task executes. If shell or plugin management is unavailable, give the host's exact UI steps from the bundled README; do not claim to have run them.

Read the bundled .mcp.json and compare its explicit endpoint with the user's existing Veloci connection. If connected to a different gateway, stop: Do not install or enable a mismatched package, switch endpoints, or infer tenant configuration. The public ArcticRexOrg/veloci-plugins beta is configured for https://test.arcticrex.com/mcp/veloci. Other gateways require their own explicitly configured package.

Inspect the host's installed plugin list and enabled components. If already installed, check the existing Veloci plugin instead of installing a duplicate. Connect only Veloci using the user's own account. An existing CLI authenticated as the real user can perform supported checks; do not invent CLI commands, service credentials, or authentication bypasses. Verify the host's current hook trust state and any managed policy; never bypass trust, enable forbidden hooks, or equate package presence with authorization. In Codex CLI the user reviews current definitions with /hooks; changed definitions require renewed trust.

Where a local Codex or Claude Code profile is established and shell execution is available, use the bundled scripts/check.py with --host codex or --host claude-code for read-only inspection. Resolve it relative to this skill's directory (../../scripts/check.py), quoting paths. This script cannot verify host trust or OAuth. Python 3 is needed only for explicit checks/migration. Do not run local profile checks against a guessed Cowork/Work profile.

Only if the user explicitly requested migration, and the plugin is enabled and trusted, run the same script with --migrate. This removes recognized arcrex/standalone task hooks and preserves unrelated hooks. The bundled remove-legacy-hooks.py requires explicit --remove and cannot install a hook; never run migration without the user’s request. Never migrate during SessionStart. Avoid two active Veloci MCP connections: after checking the replacement, have the user remove an obsolete connection through the host UI. Do not modify AGENTS.md or CLAUDE.md.

Run init once for activation or troubleshooting, not at every session. Skill naming and the MCP init prompt's presentation are host-controlled; do not promise a literal /init command or replace the host's built-in initialization. The session hook delivers canonical instructions automatically only when the host loads and trusts it.

Start a fresh session and request ordinary substantive work without mentioning tracking. Inspect actual canonical instruction delivery, verify task title/ID at opening, the same ID on continuation, and a successful complete_task result after actual completion. Unfinished work stays in progress; do not write routine progress updates or perform redundant readbacks unless explicitly asked. Never manufacture completion to pass a check. Report installation, connection, authentication, trust, instruction loading, and observed task behavior separately; anything unobserved remains not verified.

This beta requires a POSIX execution environment with the bundled script available. Cowork and ChatGPT Work each need their own runtime verification; desktop installation does not deploy scripts into hosted execution. Separate devices/profiles need separate installation. Package validation alone never proves runtime support.
