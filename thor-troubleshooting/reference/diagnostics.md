# Diagnostics

## thor-util diagnostics

The primary diagnostic tool for THOR issues.

### Basic Usage

```bash
# Collect diagnostics (works while THOR is running or after)
thor-util diagnostics

# Collect with debug re-run (monitors for interference)
thor-util diagnostics --run

# Custom output location
thor-util diagnostics --output /path/to/diagnostics.zip
```

### What It Collects

- System information (OS, CPU, RAM, disk)
- THOR configuration files
- Recent log files
- License information (sanitized)
- Running process list
- Resource usage statistics
- ThorDB statistics (if available)

### When to Use Each Mode

| Situation | Command |
|-----------|---------|
| THOR currently stuck | `thor-util diagnostics` (from another terminal) |
| THOR finished but had issues | `thor-util diagnostics` |
| Need to reproduce issue | `thor-util diagnostics --run` |
| Suspect AV/EDR interference | `thor-util diagnostics --run` |

The `--run` flag re-executes the last scan command with debug logging and monitors for external process interference (AV/EDR signals).

## Debug Mode

Run THOR with verbose debugging:

```bash
thor64.exe --debug -p C:\path
```

Produces detailed output including:
- Module start/stop times
- File processing details
- Rule matching information
- Resource usage

### Targeted Debug

Debug specific modules:

```bash
# Debug only Filescan module
thor64.exe --debug -a Filescan -p C:\path

# Debug with all output
thor64.exe --debug --printall -a Filescan -p C:\temp
```

## CTRL+C Interrupt Menu

During any scan, press **CTRL+C** to access:

1. Currently scanned element
2. Continue/abort options

Use this to identify:
- Which element is causing slowness
- Whether the scan is progressing
- If THOR is responsive

## ThorDB Statistics

THOR maintains a SQLite database with scan statistics.

**Location:**
- Windows: `C:\ProgramData\thor\thor10.db`
- Linux: `/var/lib/thor/thor10.db` or `~/.thor/thor10.db`

**View with SQLiteBrowser:**
1. Download: https://sqlitebrowser.org/
2. Open `thor10.db`
3. Check `statistics` table for slow elements

**Key tables:**
- `scans`: Scan history
- `statistics`: Element processing times
- `findings`: Previous findings (for diff mode)

## Log Analysis

### Text Log Fields

Key fields to check in THOR logs:

```
MODULE: Which component generated the message
LEVEL: Info/Notice/Warning/Alert/Error
TARGET: File/element being processed
TIME: Processing duration
MESSAGE: Detailed information
```

### Common Error Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `ERROR: License` | License issue | Check `.lic` file |
| `ERROR: Signature` | Corrupt signatures | `thor-util update --force` |
| `WARN: Timeout` | YARA timeout | `--yara-timeout 180` |
| `WARN: Skipped` | File too large | `--max_file_size` increase |
| `ERROR: Permission` | Access denied | Run as admin/root |

## System Diagnostics

### Windows

```powershell
# Check THOR process
Get-Process thor64 | Select-Object *

# Check memory
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check disk space
Get-PSDrive -PSProvider FileSystem
```

### Linux

```bash
# Check THOR process
ps aux | grep thor

# Check memory
free -h
cat /proc/meminfo

# Check disk space
df -h

# Check I/O
iostat -x 1 5
```

### macOS

```bash
# Check THOR process
ps aux | grep thor

# Check memory
vm_stat

# Check disk
df -h
```

## Bottleneck Identification

### CPU Bottleneck

Symptoms:
- High CPU usage
- Scan progressing but slow

Solutions:
- `--threads` adjustment
- `--lowprio` / `--verylowprio`
- `--cpulimit` if sharing with production workload

### Memory Bottleneck

Symptoms:
- Swap usage high
- THOR killed by OOM
- System slowdown

Solutions:
- `--threads` reduction (memory scales with threads)
- `--max_file_size` reduction
- `--minmem` adjustment
- Close other applications

### Disk I/O Bottleneck

Symptoms:
- Low CPU but slow progress
- High disk wait times

Solutions:
- `--lowioprio`
- Scan from faster storage
- Avoid scanning network shares

### Network Bottleneck

Symptoms:
- Stuck on network paths
- Timeouts

Solutions:
- Exclude network shares
- Use `-p` for local paths only
- Check network connectivity

## Support Information

When contacting Nextron support, provide:

1. **diagnostics.zip** from `thor-util diagnostics`
2. THOR version: `thor64.exe --version`
3. Operating system and version
4. License type (lab, workstation, server)
5. Exact command that caused issues
6. Description of expected vs actual behavior

## Quick Troubleshooting Checklist

1. [ ] Is THOR running? (`ps` / `tasklist`)
2. [ ] Does CTRL+C respond?
3. [ ] What element is it processing?
4. [ ] Is AV/EDR excluded?
5. [ ] Are there disk/memory/CPU constraints?
6. [ ] Is the license valid?
7. [ ] Are signatures up to date?
8. [ ] Did `thor-util diagnostics` reveal anything?
