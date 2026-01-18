# Module Notes

THOR has 30+ modules, each scanning different system aspects. Understanding which module produced a finding helps contextualize it.

## File System Modules

### Filescan
Most common source of findings. Scans files on disk.

Key indicators:
- `TARGET`: Full file path
- `HASH`: MD5/SHA1/SHA256
- `SIZE`: File size in bytes

Follow-up: Check file metadata, submit to sandbox, review with hex editor.

### ArchiveScan
Scans inside archives (ZIP, RAR, 7z, etc.).

Target format: `archive.zip|internal/path/file.js`

Note: Findings inside archives need extraction for deeper analysis.

### MFT (Master File Table)
Windows NTFS metadata analysis. Finds deleted files, timestomping.

Key indicators:
- `MFT_RECORD`: Record number
- `SI_*` vs `FN_*`: $STANDARD_INFORMATION vs $FILE_NAME timestamps

Timestomping: SI timestamps manipulated, FN timestamps original.

## Memory/Process Modules

### ProcessCheck
Running process analysis. Memory scanning, handle enumeration.

Key indicators:
- `PID`: Process ID
- `PROCESS_NAME`: Executable name
- `COMMAND_LINE`: Full command line
- `PARENT`: Parent process

Follow-up: Memory dump, process tree analysis, handle review.

### Mutex / Handles
Named synchronization objects. Malware often creates unique mutexes.

Key indicators:
- `MUTEX_NAME` / `HANDLE_NAME`
- Associated process

### Pipes
Named pipe analysis. Used for IPC, C2 communication.

Key indicators:
- `PIPE_NAME`
- Connected processes

## Registry Modules

### RegistryChecks
Windows Registry analysis for persistence, configuration.

Key indicators:
- `REG_KEY`: Full registry path
- `REG_VALUE`: Value name
- `REG_DATA`: Value content

Common persistence locations:
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- Services, Scheduled Tasks references

### SHIMCache
Application compatibility cache. Shows executed programs.

Key indicators:
- `SHIM_PATH`: Executed file path
- `SHIM_MODIFIED`: Last modified timestamp

Note: Presence in SHIMCache indicates execution (or execution attempt).

## Log Modules

### Eventlog
Windows Event Log analysis with Sigma rules.

Key indicators:
- `EVENT_ID`: Windows Event ID
- `CHANNEL`: Log channel (Security, System, etc.)
- `SIGMA_RULE`: Triggered Sigma rule

Common high-value Event IDs:
- 4624/4625: Logon success/failure
- 4688: Process creation
- 7045: Service installation
- 1102: Audit log cleared

### LogScan
Generic log file analysis (text logs, application logs).

Parses: Apache, IIS, application logs.

## Network Modules

### DNSCache
DNS resolver cache analysis.

Key indicators:
- `DNS_NAME`: Queried domain
- `DNS_TYPE`: Record type
- `DNS_DATA`: Resolution result

### NetworkShares
SMB/network share enumeration.

### NetworkSessions
Active network sessions.

### Firewall
Windows Firewall rule analysis.

## Persistence Modules

### Autoruns
Auto-start extensibility points (ASEPs).

Covers: Run keys, services, scheduled tasks, browser extensions, etc.

### ServiceCheck
Windows service analysis.

Key indicators:
- `SERVICE_NAME`
- `SERVICE_PATH`: Binary path
- `SERVICE_START_TYPE`

### ScheduledTasks
Task Scheduler analysis.

Key indicators:
- `TASK_NAME`
- `TASK_ACTION`: What runs
- `TASK_TRIGGER`: When it runs

### WMIStartup
WMI persistence (event subscriptions).

### AtJobs
Legacy AT scheduler jobs.

### Cron (Linux)
Cron job analysis.

## User Modules

### Users
Local user account enumeration.

### UserDir
User profile directory analysis.

### LoggedIn
Currently logged-in users.

### LSASessions
LSA session information.

## Integrity Modules

### Rootkit
Rootkit detection techniques.

### Integritycheck (Linux)
Package manager integrity verification.

### Timestomp
Timestamp manipulation detection.

## Module Selection

Run specific modules only:
```bash
thor64.exe -a Filescan -a ProcessCheck -a Eventlog
```

Disable specific modules:
```bash
thor64.exe --noprocs --noreg --noeventlog
```

## Module Availability by Mode

| Module | Default | Quick | Soft | Intense |
|--------|---------|-------|------|---------|
| Filescan | Yes | Yes | Yes | Yes |
| ProcessCheck | Yes | Yes | No | Yes |
| Eventlog | Yes | No | Yes | Yes |
| MFT | No | No | No | Yes |
| RegistryChecks | Yes | Yes | Yes | Yes |
| Mutex | Yes | Yes | No | Yes |

See THOR documentation for complete matrix.
