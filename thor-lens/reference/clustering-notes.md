# Clustering Notes

THOR Lens uses clustering to group related findings and help analysts prioritize investigation.

## Clustering Approaches

### Relationship-Based Clustering

Groups elements that are directly related:
- Files within the same archive
- Parent/child process relationships
- Registry keys under common paths
- Files in the same directory

### Detection-Based Clustering

Groups elements that triggered similar detections:
- Same YARA rule matches
- Same IOC type matches
- Similar anomaly scores
- Common signature families

### Temporal Clustering

Groups elements with related timestamps:
- Similar creation times
- Similar modification times
- Activity within investigation timeframe
- Epoch-matched elements

### Path-Based Clustering

Groups elements by location:
- Same directory
- Same drive/partition
- User profile groupings
- System vs user space

## Cluster Prioritization

When reviewing clusters, prioritize by:

1. **Cluster size** - Larger clusters may indicate widespread activity
2. **Highest score** - Clusters containing high-confidence findings
3. **Connection density** - Highly interconnected elements
4. **Temporal concentration** - Activity bursts in short timeframes

## Investigation Strategies

### Hub-and-Spoke

Start from a high-confidence finding and explore connected elements:
1. Identify central finding (high score, known-bad signature)
2. Follow relationships to connected elements
3. Evaluate each connected element
4. Expand investigation based on new findings

### Cluster Review

Systematically review clusters from most to least suspicious:
1. Sort clusters by priority criteria
2. Review top clusters first
3. Mark elements as investigated/cleared/suspicious
4. Drill into suspicious clusters

### Anomaly Focus

Focus on elements that don't fit patterns:
1. Identify outlier elements (unusual paths, timestamps)
2. Check for isolated high-score findings
3. Look for unusual relationship patterns
4. Investigate elements with unique characteristics

## Filtering Clusters

Reduce noise by filtering:
- Exclude known-good paths
- Exclude low-score notices
- Focus on specific modules (Filescan, ProcessCheck)
- Time-bound to investigation window

## Cluster Export

Export cluster data for:
- Reporting and documentation
- Timeline analysis tools
- IOC extraction
- Evidence preservation

## Best Practices

1. **Start broad, narrow down** - Begin with overview, then drill into interesting clusters
2. **Document decisions** - Record why clusters were cleared or flagged
3. **Cross-reference** - Compare clusters across multiple scans/systems
4. **Don't ignore small clusters** - Single high-confidence findings matter
5. **Revisit with new context** - Re-evaluate clusters as investigation progresses
