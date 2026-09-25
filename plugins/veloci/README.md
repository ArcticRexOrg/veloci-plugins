# Veloci by ArcticRex — 0.3.0 beta

Connect goals, reconcile commitments, and keep work moving with Veloci. Review goals and their tasks to plan your next steps, reconcile evidence from your notes with existing commitments, and save progress when requested.

## Try Veloci

- Show my goals and the open work connected to them so I can plan my next steps.
- Reconcile the commitments in these notes with my existing work.
- Save my progress and show what remains on this task.

## Enable automatic task tracking

Install Veloci once in each execution environment to load canonical task instructions in fresh agentic sessions. Connect with your own Veloci account, review permissions and trust, then use the init skill once to check setup. Do not invoke init every session.

This package connects to https://veloci.arcticrex.com/mcp/veloci. No credentials are included. The public marketplace beta below targets https://veloci.arcticrex.com/mcp/veloci only. If your gateway differs, do not install the beta or switch your account; use a package explicitly configured for your gateway.

## Claude Code

Run /plugin marketplace add ArcticRexOrg/veloci-plugins, then /plugin install veloci@arcticrex. Choose user scope. Run /reload-plugins if the installation summary requests it. Review plugin permissions and hook settings in the host, then start a new session.

## Claude Cowork

Open Customize → Plugins → Add marketplace, enter https://github.com/ArcticRexOrg/veloci-plugins, select Veloci and Install, then authenticate its connector when prompted. Confirm its components are enabled. Establish the actual execution host before inspecting files; do not assume access to desktop settings. Verify instruction delivery inside a fresh Cowork task.

## Codex

Run codex plugin marketplace add ArcticRexOrg/veloci-plugins in the actual local execution environment. Restart the desktop app, open Plugins Directory, select ArcticRex, and install Veloci. In Codex CLI use /plugins to install from the registered marketplace. Review and trust the current definitions with /hooks; changed definitions need renewed trust. Administrators may disable hooks or allow only managed hooks. After installation or an update, quit and reopen Codex desktop and start a fresh task; in Codex CLI, start a new session.

## ChatGPT Work

For local desktop execution, run codex plugin marketplace add ArcticRexOrg/veloci-plugins locally, restart the desktop app, open Plugins Directory, select ArcticRex and install Veloci. For a workspace import, an authorized admin uses Admin → Plugins → Add → Import marketplace with https://github.com/ArcticRexOrg/veloci-plugins, authorizes GitHub, imports, and sets Available/Installed policy; members still authenticate. This MCP bundle is Desktop only. Account eligibility must be checked. Desktop installation does not deploy scripts to hosted execution; cloud support remains unverified until the actual runtime delivers and executes the trusted definitions. Do not claim a public MCP/skills listing proves that delivery.

Connect only Veloci with the user's own account, complete the host's authentication and trust steps, and invoke the plugin's init skill once to check setup. An existing CLI authenticated as the real user can be used for supported checks; do not create service credentials or bypass authentication. Do not bypass trust or managed policy. Avoid two active Veloci MCP connections; remove an obsolete connection through the host UI only after checking the replacement. The MCP init prompt's presentation is host-controlled; a literal /init command is not guaranteed, and it does not replace a host's built-in /init. Do not require init on every session. Installation and connection are not evidence that canonical instructions loaded. Never install standalone hooks or modify AGENTS.md or CLAUDE.md from this flow.

## Verify a fresh session

Automatic tracking is not verified. In a fresh session, request ordinary substantive work without mentioning tracking. Inspect evidence that the canonical Veloci instructions loaded, then verify an opening task title/ID, continuation of the same task ID, and a successful complete_task result when the tracked work is actually finished. Routine progress updates and repeated readbacks are not required. Complete only finished work. Report installation, authentication, trust, instruction delivery, and task behavior separately; missing evidence remains unverified. Each execution device/profile and Cowork or Work runtime needs its own verification.

The session hook prints the canonical task instructions. It makes no network requests, installs nothing, and changes no files. An agent's compliance must be observed. This beta needs a POSIX execution environment with its bundled script available; no public directory listing or cloud execution verification is implied.

## Existing installation and updates

If Veloci is already installed, use init to check its connection and trust instead of installing a duplicate. Update through the host plugin manager, review any changed permissions/hook definitions, and repeat fresh-session verification.

For an explicitly requested migration of an existing local Codex setup, run python3 scripts/check.py --host codex from this plugin directory. Use --host claude-code for Claude Code. Only after enabling and trusting the plugin, append --migrate to remove recognized old task hooks. Python 3 is required for this explicit check/removal only. Unrelated hooks are preserved. For an isolated fixture, add --home /absolute/test/home. The remove-legacy-hooks.py helper can only remove recognized legacy hooks.

Uninstall through the host plugin manager to remove the plugin hook and bundled MCP connection. Migration does not restore old hooks on uninstall.
