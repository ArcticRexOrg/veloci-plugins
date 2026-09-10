#!/usr/bin/env python3
"""Inspect standalone task hooks; --migrate explicitly removes them for plugin use."""
import argparse
import json
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("codex", "claude-code"), required=True)
    parser.add_argument("--home", help="Isolated test home; ignores host configuration overrides")
    parser.add_argument("--migrate", action="store_true", help="Remove recognized standalone task hooks; run only after enabling and trusting the plugin")
    args = parser.parse_args()
    remover = Path(__file__).with_name("remove-legacy-hooks.py")
    contract = runpy.run_path(str(remover))
    home = Path(args.home).absolute() if args.home else Path.home()
    root = home / (".codex" if args.host == "codex" else ".claude")
    variable = "CODEX_HOME" if args.host == "codex" else "CLAUDE_CONFIG_DIR"
    if not args.home and os.environ.get(variable):
        root = Path(os.environ[variable]).expanduser().absolute()
    settings = root / ("hooks.json" if args.host == "codex" else "settings.json")
    emitter = root / "hooks" / "veloci-mcp-session-start.sh"
    config = json.loads(settings.read_text(), object_pairs_hook=contract["unique_object"]) if settings.exists() else {}
    contract["validate"](config)
    command = "/bin/sh " + shlex.quote(str(emitter))
    count = sum(contract["owned"](hook, command) for group in config.get("hooks", {}).get("SessionStart", []) for hook in group["hooks"])
    if args.migrate:
        command = [sys.executable, str(remover), "--host", args.host, "--remove"]
        if args.home:
            command += ["--home", args.home]
        subprocess.run(command, check=True, stdout=subprocess.PIPE)
    print(json.dumps({"host": args.host, "standalone_hooks": count, "migration": "removed" if args.migrate else "not_requested", "runtime_verified": False, "next_step": "Verify plugin enabled, Veloci connected, and hook trusted in the host. Start a fresh session and verify task opening and final saved-state readback."}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print("Veloci check failed: " + str(error), file=sys.stderr)
        sys.exit(1)
