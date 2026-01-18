---
name: thor-lens
description: THOR Lens workflows for visualizing and clustering scan results. Requires THOR v11 audit trail output (not available in v10).
---

# THOR Lens Skill

THOR Lens is a visualization and analysis tool for THOR scan results that helps analysts explore relationships between findings, cluster suspicious elements, and discover lateral connections.

**Critical Requirement**: THOR Lens requires the audit trail output from THOR v11. This feature is not available in THOR v10.

## Prerequisites Check

Before starting a THOR Lens workflow:

1. Verify THOR version is v11 or later
2. Confirm audit trail was enabled during scan (`--audit-trail`)
3. Locate the audit trail file (`.json.gz` format)

## When to Use THOR Lens

- Multiple scan results need correlation
- Looking for patterns across findings
- Investigating lateral movement or related artifacts
- Visualizing relationships between suspicious elements
- Clustering analysis for triage prioritization

## References

- [Overview](reference/overview.md) - THOR Lens concepts and capabilities
- [Audit Trail Requirements](reference/audit-trail-requirements.md) - Required THOR configuration
- [Clustering Notes](reference/clustering-notes.md) - How clustering works

## Examples

- [Minimal Workflow](examples/minimal-workflow.md) - Basic THOR Lens usage

## Workflow Rules

1. Always verify THOR v11 was used before attempting THOR Lens analysis
2. Ensure audit trail file is complete (scan finished successfully)
3. Check file integrity (gzip should decompress without errors)
4. Large audit trails may require significant memory for processing
