---
name: thor-log-analysis
description: Interpret THOR scan results and explain what findings mean. Use when the user pastes THOR log lines, shares a log file, or asks how to triage Notices/Warnings/Alerts.
---
# THOR Log Analysis Skill

Goal: turn raw THOR output into an investigation plan.

Rules
- Triage order: Alerts -> Warnings -> then high-signal Notices (don’t drown in noise).
- Group by detection type/module (YARA, Sigma, IOC, Anomaly) and by file/path.
- For each relevant finding: explain what it is, why it triggered, and what to verify next.
- Be explicit when something is likely benign (common false positives).

Use these references when needed
- Scoring and priorities: reference/scoring-and-priorities.md
- Common false positives: reference/common-fps.md
- Module notes: reference/module-notes.md

Optional helper script
- If user provides a log file path, run scripts/summarize_thor_log.py to extract a compact summary (top findings, counts, modules).

Output format
- 5-15 line summary: what’s going on, what stands out
- Findings table-like bullets: (score, type/module, target, why it matters)
- Next steps: 3-7 concrete follow-ups
