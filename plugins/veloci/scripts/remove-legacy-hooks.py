#!/usr/bin/env python3
"""Remove recognized legacy Veloci task hooks; never installs a hook."""
import argparse
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile

MARKER = "#!/bin/sh\n# Veloci MCP task reminder, policy 1\n"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate configuration key: " + key)
        result[key] = value
    return result


def validate(config):
    if not isinstance(config, dict) or not isinstance(config.get("hooks", {}), dict):
        raise ValueError("settings and hooks must be JSON objects")
    groups = config.get("hooks", {}).get("SessionStart", [])
    if not isinstance(groups, list):
        raise ValueError("SessionStart must be an array")
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError("SessionStart groups must contain a hooks array")
        if any(not isinstance(hook, dict) for hook in group["hooks"]):
            raise ValueError("hook entries must be JSON objects")


# Ownership contract shared with the CLI session-hook installer: the designated
# MCP emitter argv or exactly arcrex session-hook <supported host>. Arbitrarily
# renamed legacy binaries cannot be identified safely by this removal helper.
def owned(hook, command):
    if hook.get("type") != "command":
        return False
    value = hook.get("command", "")
    if not isinstance(value, str):
        return False
    try:
        args = shlex.split(value)
    except ValueError:
        return False
    return args == shlex.split(command) or (len(args) == 3 and Path(args[0]).name == "arcrex"
            and args[1] == "session-hook" and args[2] in ("codex", "claude-code"))


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".veloci-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as output:
            output.write(text)
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("codex", "claude-code"), required=True)
    parser.add_argument("--home", help="Isolated home for verification; ignores host configuration overrides")
    parser.add_argument("--remove", action="store_true", required=True, help="Explicitly remove recognized legacy task hooks")
    args = parser.parse_args()
    home = Path(args.home).absolute() if args.home else Path.home()
    root = home / (".codex" if args.host == "codex" else ".claude")
    config_variable = "CODEX_HOME" if args.host == "codex" else "CLAUDE_CONFIG_DIR"
    if not args.home and os.environ.get(config_variable):
        root = Path(os.environ[config_variable]).expanduser().absolute()
    settings = root / ("hooks.json" if args.host == "codex" else "settings.json")
    emitter = root / "hooks" / "veloci-mcp-session-start.sh"
    command = "/bin/sh " + shlex.quote(str(emitter))
    # Check destinations before any read or mutation, including broken links.
    for path in (home, root, settings, emitter.parent, emitter):
        if path.is_symlink():
            raise ValueError("symbolic link at " + str(path))
    if emitter.exists() and not emitter.read_text().startswith(MARKER):
        raise ValueError("an unrelated file occupies " + str(emitter))
    existed = settings.exists()
    config = json.loads(settings.read_text(), object_pairs_hook=unique_object) if existed else {}
    validate(config)
    hooks = config.setdefault("hooks", {})
    groups = []
    for group in hooks.get("SessionStart", []):
        kept = [hook for hook in group["hooks"] if not owned(hook, command)]
        if kept or not group["hooks"]:
            groups.append(dict(group, hooks=kept))
    if groups:
        hooks["SessionStart"] = groups
    else:
        hooks.pop("SessionStart", None)
    if not hooks:
        config.pop("hooks", None)
    if existed:
        write_atomic(settings, json.dumps(config, indent=2) + "\n")
    emitter.unlink(missing_ok=True)
    print(json.dumps({"host": args.host, "status": "removed", "policy_version": "1", "settings": str(settings), "verification": "Open a fresh session, accept the host's hook trust prompt if shown, and verify automatic tracking."}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print("Refusing removal: " + str(error), file=sys.stderr)
        sys.exit(1)
