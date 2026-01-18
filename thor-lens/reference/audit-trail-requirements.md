# Audit Trail Requirements

**Note: THOR Lens requires the audit trail log produced by THOR v11; this audit trail output is not available in THOR v10.**

## Version Requirement

THOR Lens exclusively uses the audit trail output format introduced in THOR v11. The enhanced audit trail schema in v11 includes:
- Unique element identifiers
- Relationship references between elements
- Complete timestamp information
- Structured scoring data

THOR v10 does not produce audit trail output in the format required by THOR Lens.

## Generating Compatible Audit Trails

### Basic Command

```bash
./thor-linux-64 --audit-trail <hostname>_audit.json.gz [other flags]
```

### Lab Mode (Recommended)

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j HOSTNAME \
  --audit-trail /cases/HOSTNAME_audit.json.gz \
  -e /cases/reports
```

### Memory Dump Scan

```bash
./thor-linux-64 --lab \
  --image_file /path/to/memory.dmp \
  --audit-trail /cases/HOSTNAME_audit.json.gz \
  -j HOSTNAME \
  -e /cases/reports
```

## Audit Trail Contents

The audit trail captures:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier for each scanned element |
| `object` | The scanned element (file path, registry key, etc.) |
| `timestamps` | All timestamps associated with the element |
| `reasons` | Detection reasons with individual scores |
| `references` | Links to related elements (parent, contained files, etc.) |

## File Format

- **Extension**: `.json.gz` (gzip-compressed)
- **Format**: Newline-delimited JSON (NDJSON)
- **Encoding**: UTF-8

## Size Considerations

Audit trails can be large because they record ALL scanned elements, not just findings:
- Typical system scan: 100MB - 1GB compressed
- Full forensic image: 500MB - 5GB compressed
- Memory dump: 50MB - 500MB compressed

Ensure sufficient storage and memory for processing.

## Verification

### Check Audit Trail Integrity

```bash
# Verify gzip integrity
gzip -t audit.json.gz

# View first few entries
zcat audit.json.gz | head -5

# Count entries
zcat audit.json.gz | wc -l
```

### Required Fields Check

Each entry should contain at minimum:
- `id` field
- `object` field
- Valid JSON structure

## Common Issues

### Empty Audit Trail

Causes:
- Scan aborted before completion
- Disk space exhausted
- Write permission errors

Solution: Re-run scan with sufficient resources.

### Corrupt Audit Trail

Causes:
- Incomplete write (crash/kill during scan)
- Transfer corruption

Solution: Check gzip integrity, re-transfer or re-scan.

### Wrong THOR Version

Symptom: Audit trail missing required fields for THOR Lens.

Solution: Upgrade to THOR v11 (`thor-util upgrade --techpreview`) and re-scan.
