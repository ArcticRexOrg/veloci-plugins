# Veloci by ArcticRex

Connect your agent to your Veloci workspace: set and review goals, reconcile commitments from your notes, and keep progress tied to the work that matters. The plugin also loads the shared work-tracking instructions when a supported agentic session starts.

Try “Show my goals and open commitments so we can decide what matters next,” or “Reconcile these notes with my existing commitments.” Tools depend on your workspace's available capabilities. Plan your week, connect goals to commitments, and review progress with Veloci.

**Beta for existing Veloci accounts on test.arcticrex.com.** This source is maintained by ArcticRex. It is not an official vendor directory listing or a verified badge. Installation does not grant workspace access. Cowork and ChatGPT Work still need a real installation and fresh-session verification; do not assume the CLI test results establish their behavior.

**Public beta marketplace.** Install from the ArcticRex repository using the steps below. If Veloci is already installed, check its endpoint, enabled components, authentication, trust, and fresh-session behavior before reinstalling.

If your existing Veloci connection uses a different gateway, do not install this test beta or switch your account. Use a package explicitly configured for your gateway.

## Claude Cowork

1. Open **Customize → Plugins → Add marketplace**.
2. Enter **https://github.com/ArcticRexOrg/veloci-plugins**.
3. Select **Veloci**, install it, and sign in to your Veloci account.
4. Enable the plugin components, start a new Cowork task, and ask **“Run Veloci init to check automatic task tracking.”**

## Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add ArcticRexOrg/veloci-plugins
/plugin install veloci@arcticrex
```

Choose user scope. Sign in to Veloci when prompted. Reload plugins if the installation summary requests it, start a new session, and invoke the plugin’s init skill once using the host’s supported presentation. A literal `/init` command is not guaranteed and does not replace the host’s built-in initialization.

## Codex and local ChatGPT Work

Register the marketplace in a local terminal:

```sh
codex plugin marketplace add ArcticRexOrg/veloci-plugins
```

Restart the desktop app. In **Plugins Directory**, select **ArcticRex**, install **Veloci by ArcticRex**, and connect your account. Review and trust its current hook definition where prompted (`/hooks` in Codex CLI). Start a new local task and ask **“Run Veloci init to check automatic task tracking.”** A web installation does not deploy scripts to a separate hosted environment.

## Know when it works

Init is a one-time check, not a command to repeat before every session. After setup, start ordinary work in a fresh session without mentioning tracking. Your agent should show the task title and ID, save unfinished progress, and read back the saved task state when it finishes. A task that is still unfinished must stay open.

The check reports connection, installation, trust, and observed instruction delivery separately. If it cannot prove instructions loaded, it reports that. Installation alone is not verification. Remote control of the same computer uses that computer's setup; a separate agent or execution environment needs its own setup.

## What the plugin does

The plugin connects to `https://test.arcticrex.com/mcp/veloci` using your own account. Its startup script only prints the Veloci task instructions; it performs no network request and changes no files. The agent uses Veloci tools under the permissions you grant. No arcrex binary or edits to AGENTS.md/CLAUDE.md are required.

The removal-only `scripts/remove-legacy-hooks.py` helper requires explicit `--remove`; the `scripts/check.py --migrate` flow calls it. No standalone installer is bundled. The optional migration removes only recognized old standalone task hooks when you explicitly request migration after the plugin is enabled and trusted. It preserves unrelated hooks. Do not enable duplicate standalone and plugin task hooks. Use the host connection UI to remove an obsolete duplicate MCP connection after verifying the replacement.

## Update or remove

Use your host's plugin manager to update or uninstall Veloci. Updated hook definitions may require renewed trust. Start a fresh session to verify the update. Uninstalling does not restore a standalone hook removed during migration or delete your Veloci tasks.

[ArcticRex](https://www.arcticrex.com) · [Contact](mailto:contact@arcticrex.com)

Report installation issues through this repository's issues. Include host/version and which setup step failed; do not post tokens, private tasks, or account data.
