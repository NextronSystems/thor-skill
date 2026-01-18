# THOR Lens Minimal Workflow

A basic workflow for using THOR Lens with a single scan.

## Step 1: Run THOR v11 with Audit Trail

```bash
./thor-linux-64 --lab \
  -p /mnt/suspect_image \
  --virtual-map /mnt/suspect_image:C \
  -j WORKSTATION01 \
  --audit-trail /cases/WORKSTATION01_audit.json.gz \
  -e /cases/reports
```

**Key flags:**
- `--audit-trail`: Enables audit trail output (REQUIRED for THOR Lens)
- Must be THOR v11 (v10 does not support audit trail)

## Step 2: Verify Audit Trail

```bash
# Check file exists and has content
ls -lh /cases/WORKSTATION01_audit.json.gz

# Verify integrity
gzip -t /cases/WORKSTATION01_audit.json.gz && echo "OK"

# Preview content
zcat /cases/WORKSTATION01_audit.json.gz | head -3 | jq .
```

## Step 3: Import into THOR Lens

Load the audit trail file into THOR Lens for analysis.

## Step 4: Initial Triage

1. Review summary statistics (total elements, findings by level)
2. Identify high-score clusters
3. Note any Alert-level findings

## Step 5: Investigate Clusters

For each priority cluster:

1. Review the central/highest-score element
2. Examine related elements in the cluster
3. Follow relationships to connected elements
4. Document findings and decisions

## Step 6: Follow Rabbit Holes

From interesting findings:

1. Check what files were in the same archive
2. Look at what other findings share the same path
3. Check temporal neighbors (same timeframe)
4. Explore process relationships (if available)

## Step 7: Export Results

Export:
- List of investigated elements
- IOCs discovered
- Timeline of suspicious activity
- Cluster summaries for reporting

## Example Scenario

**Initial finding**: YARA match for webshell in `/mnt/suspect_image/inetpub/wwwroot/`

**THOR Lens investigation:**

1. Cluster shows 3 other files in same directory with similar timestamps
2. Following relationships: All files created within 5 minutes
3. Temporal clustering: Activity spike at 2024-01-15 03:42 UTC
4. Path analysis: Several other suspicious files in `wwwroot` subdirectories

**Outcome**: Identified initial access vector and 12 related webshell variants.

## Quick Reference

| Task | Action |
|------|--------|
| Generate audit trail | `--audit-trail file.json.gz` with THOR v11 |
| Verify file | `gzip -t file.json.gz` |
| Preview content | `zcat file.json.gz | head | jq .` |
| Count elements | `zcat file.json.gz | wc -l` |
