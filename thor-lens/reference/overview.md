# THOR Lens Overview

THOR Lens is an analysis and visualization companion for THOR scan results that enables deeper investigation through relationship mapping, clustering, and pattern discovery.

## Core Capabilities

### Relationship Visualization

THOR Lens maps relationships between scanned elements:
- Archive contents and their parent containers
- Extracted files and their sources
- Process hierarchies (parent/child)
- Related findings across different scan targets

### Clustering Analysis

Groups related findings to help prioritize investigation:
- Similar file characteristics
- Common detection patterns
- Temporal correlations
- Path-based groupings

### Pattern Discovery

Identifies patterns that may not be obvious in raw logs:
- Repeated indicators across systems
- Lateral movement traces
- Campaign-level artifacts
- False positive patterns

## Data Source: Audit Trail

THOR Lens consumes the audit trail output from THOR v11 scans.

**Required scan command:**
```bash
./thor-linux-64 --lab -p /target --audit-trail audit.json.gz
```

The audit trail contains:
- All scanned elements (not just detections)
- Element relationships (references)
- Timestamps for each element
- Full scoring details

## Typical Use Cases

### Multi-System Investigation

When scanning multiple systems in an incident:
1. Run THOR v11 with `--audit-trail` on each system
2. Import audit trails into THOR Lens
3. Correlate findings across systems
4. Identify common indicators and lateral movement

### Deep Dive on Single System

For thorough analysis of one compromised system:
1. Run comprehensive THOR v11 scan with audit trail
2. Import into THOR Lens
3. Explore relationships between findings
4. Follow "rabbit holes" from initial detections

### Triage Prioritization

When facing many findings:
1. Import audit trail
2. Use clustering to group related items
3. Prioritize investigation of largest/most connected clusters
4. Work outward from high-confidence findings

## Limitations

- Requires THOR v11 (audit trail not available in v10)
- Large audit trails need proportional memory
- Visualization complexity increases with data volume
- Best suited for focused investigations, not fleet-wide analysis
