#!/bin/sh
# Veloci MCP task reminder
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Use Veloci for substantive work; status questions need no task.\n\nAt the start, find the matching task or create one under the relevant goal. Call start_task and announce its title and ID once, then keep that ID bound.\n\nWhen the tracked work is actually complete — ships, merges, or lands — call complete_task and report the result."}}'
