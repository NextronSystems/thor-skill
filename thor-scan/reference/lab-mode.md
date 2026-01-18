# Lab Mode

Lab mode (`--lab`) is designed for forensic analysis of mounted disk images and memory dumps. Requires a Forensic Lab License.

## What `--lab` Enables Automatically

- Intense mode (every file scanned, 200MB limit)
- Multi-threading (all CPU cores)
- No resource control (`--norescontrol`)
- No double-check for other THOR instances (`--nodoublecheck`)
- No ThorDB
- Cross-platform IOC application
- Sigma minimum level: Medium

## Key Lab Mode Flags

### Virtual Drive Mapping (`--virtual-map`)

Maps mounted image paths to original paths for accurate reporting.

```bash
# Windows: F: drive was originally C:
--virtual-map F:C

# Linux: mount point to original root
--virtual-map /mnt/image1:/

# Windows image mounted on Linux
--virtual-map /mnt/image1:C
```

### Hostname Override (`-j`)

Replace forensic workstation hostname with original system name in logs.

```bash
-j YOURHOST
```

### Output Directory (`-e`)

Write all outputs (HTML, TXT, CSV, JSON) to specified folder.

```bash
-e /path/to/reports
```

## Standard Lab Command Templates

### Mounted Windows Image (on Windows)
```bash
thor64.exe --lab -p S:\ --virtual-map S:C -j YOURHOSTNAME -e C:\reports
```

### Mounted Windows Image (on Linux)
```bash
./thor-linux-64 --lab -p /mnt/image --virtual-map /mnt/image:C -j YOURHOSTNAME -e /reports
```

### Mounted Linux Image (on Linux)
```bash
./thor-linux-64 --lab -p /mnt/image --virtual-map /mnt/image:/ -j YOURHOSTNAME -e /reports
```

## Memory Dump Scanning

### Direct Memory Image Analysis
```bash
./thor-linux-64 --lab --image_file /path/to/memory.dmp -j YOURHOSTNAME -e /reports
```

DeepDive processes overlapping 3MB chunks and reports byte offsets.

### Extracted Process Dumps (from Volatility)
```bash
# First extract with Volatility:
# vol.py -f image.mem --profile=Profile memdump -D procs/

# Then scan extracted dumps:
./thor-linux-64 --lab -p /path/to/extracted/procs/ -j YOURHOSTNAME -e /reports
```

### Restore PE Files (`-r`)
```bash
./thor-linux-64 --lab --image_file memory.dmp -r /restored_files/ -e /reports
```

Restores PE files matching YARA rules to the specified directory.

## Without a Lab License

Simulate lab-like behavior (limited):
```bash
./thor-linux-64 -a Filescan --intense -p /mnt/image
```

This lacks: virtual mapping, hostname override, cross-platform IOCs, multi-threading.

## Related Lab Features

### Drop Zone Mode (`--dropzone`)
Monitor a folder for new files and auto-scan them.
```bash
thor64.exe --dropzone -p /watch/folder
```
Options: `--dropdelete` (remove after scan), `--dropzone-delay <seconds>`.

### Artifact Collector (`--collector`)
Collect system artifacts into ZIP (requires "THOR Deep Forensics" license).
```bash
thor64.exe --lab --collector -p S:\ --collector-output /artifacts/
```

## Running Multiple Lab Scans

On a multi-core forensic workstation running multiple parallel scans:
- Use `--threads 4` per scan on a 16-core system with 4 parallel scans
- Memory scales with threads × max_file_size
