---
name: thor-troubleshooting
description: Troubleshoot THOR runs that are stuck, slow, failing to start, or produce missing output. Use when the user reports freezes, long runtimes, high CPU pauses, or licensing/update issues.
---
# THOR Troubleshooting Skill

Goal: diagnose the failure mode fast and propose minimal next actions.

Rules
- Assume AV/EDR interference until disproven (especially “frozen at 98%” style reports).
- Ask for exactly the minimum needed: platform + THOR version + command used + what “stuck” means (no progress? no output?).
- Use Ctrl+C interrupt menu guidance when relevant.
- Prefer thor-util diagnostics when available.

Use these references when needed
- Stuck scans: reference/stuck-scans.md
- AV/EDR interference patterns: reference/av-edr-interference.md
- Diagnostics: reference/diagnostics.md

Optional helper script
- scripts/quick-env-check.sh: quick info dump about folder permissions, free space, CPU/RAM, and THOR files present.

Output format
- Likely cause ranking (top 3)
- Next command(s) to run
- What evidence to collect (files/log snippets) if it persists
