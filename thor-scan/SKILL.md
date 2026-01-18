---
name: thor-scan
description: Run THOR scans and propose the exact command line for Windows, Linux, or macOS. Use when the user wants to scan a host, a directory, a mounted image, or a memory dump with THOR v10/v11.
---
# THOR Scan Skill

Goal: produce a safe, reproducible THOR command line and minimal preflight checks.

Rules
- Prefer THOR v10 stable unless the user explicitly wants v11 TechPreview features.
- Always start with environment detection: OS, THOR path, license presence, and whether thor-util exists.
- Avoid “magic flags”. Explain why each non-trivial flag is used.
- Default to focusing on forensic / lab workflows; if it’s live endpoint scanning, keep it conservative.

Preflight checklist
1) Get the THOR install path (or infer from current working dir).
2) Verify binaries exist:
   - Windows: thor64.exe
   - Linux: thor-linux-64
   - macOS: thor-macosx
3) Check license files (*.lic) in THOR dir.
4) Check thor-util presence for update/diagnostics/report tasks.
5) Identify scan target type:
   - live path, mounted image, memory dump, extracted dumps
6) Choose scan mode and output location; keep outputs deterministic.

Use these references when needed
- Environment detection: reference/env-detection.md
- Scan modes overview: reference/scan-modes.md
- Forensic lab mode: reference/lab-mode.md
- Performance and threading: reference/performance.md
- Output and reports: reference/output-and-reporting.md
- Signature selectors/filters: reference/signature-filtering.md

Output format
- First line: one recommended command (single-line).
- Then: short explanation of key flags.
- Then: “If it fails” section with 2-3 likely causes and next commands to run.
