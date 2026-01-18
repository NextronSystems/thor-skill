# Signature Filtering

## Init Selector (`--init-selector`)

Load only signatures matching keyword(s). Useful for targeted threat hunting.

```bash
# Single keyword
thor64.exe --init-selector ProxyShell

# Multiple keywords (comma-separated)
thor64.exe --init-selector RANSOM,Lockbit

# Case-insensitive partial match
thor64.exe --init-selector cobalt
```

## Init Filter (`--init-filter`)

Exclude signatures matching keyword(s). Useful for suppressing known false positives.

```bash
# Filter out AutoIt-related signatures
thor64.exe --init-filter AutoIt

# Filter multiple patterns
thor64.exe --init-filter AutoIt,Nirsoft
```

## Print Signatures (`--print-signatures`)

List all available signatures (for planning selectors/filters):

```bash
thor64.exe --print-signatures > signatures.txt
```

## Sigma Ruleset Selection (v11)

Select Sigma rule severity tiers:

```bash
--sigma-ruleset core      # Minimal FP rate
--sigma-ruleset core+     # Balanced
--sigma-ruleset core++    # More coverage
--sigma-ruleset emerging_threats
--sigma-ruleset all       # Maximum coverage, higher FP
```

## Sigma Level Filtering

```bash
--sigma-level high        # Only high+ level rules
--sigma-level medium      # Medium+ (default in lab mode)
--sigma-level low         # All levels (noisy)
```

## Disable Signature Types

```bash
--nosigma    # Disable Sigma rules
--noyara     # Disable YARA rules
--nostix     # Disable STIX IOCs
--noc2       # Disable C2/IOC detection
```

## Custom Signatures

Place in `./custom-signatures/`:

### IOC Files (.txt)

Filename must include type keyword:
- `*-c2-*.txt` or `*-domains-*.txt`: IP/hostname IOCs
- `*-hash-*.txt` or `*-hashes-*.txt`: MD5/SHA1/SHA256/Imphash
- `*-filename-*.txt`: Regex filename patterns
- `*-keyword-*.txt`: String keywords
- `*-handles-*.txt`: Mutex/Event values
- `*-pipes-*.txt`: Named pipes
- `*-trusted-hash-*.txt`: Whitelist hashes

Format:
```
<hash>;<comment>
<hash>;<score>;<comment>
```

### YARA Rules (.yar, .yara)

Place in `./custom-signatures/yara/`. Use filename tags:
- `*-registry-*.yar`: Registry checks
- `*-log-*.yar`: Log/Eventlog analysis
- `*-process-*.yar` or `*-memory-*.yar`: Process memory only
- `*-keyword-*.yar`: String checks
- `*-meta-*.yar`: Metadata checks on all files

### Sigma Rules (.yml, .yaml)

Place in `./custom-signatures/sigma/`.

### STIX v2 IOCs (.json, .stix)

Place in `./custom-signatures/`.

## Encrypting Custom Signatures

Use thor-util to encrypt proprietary signatures:

```bash
thor-util encrypt ./custom-signatures/my-rules.yar
```

| Original | Encrypted |
|----------|-----------|
| .txt | .dat |
| .yar, .yara | .yas |
| .yml, .yaml | .yms |
| .json | .jsos |

## Exclude Components (v11)

Disable specific parsing components:

```bash
--exclude-component ModuleAnalysisCache
--exclude-component ICS
--exclude-component VBEDecoder
--exclude-component ShimDB
--exclude-component JumpList
```

## Practical Examples

### Hunt for Specific Threat
```bash
thor64.exe --init-selector APT29 -p C:\
```

### Reduce Noise from Known FPs
```bash
thor64.exe --init-filter AutoIt,Nirsoft,7zip -p C:\
```

### Targeted Ransomware Hunt
```bash
thor64.exe --init-selector RANSOM --sigma-level high -p C:\
```

### Run with Custom IOCs Only
```bash
# Place IOCs in ./custom-signatures/, then:
thor64.exe --nostix -p /target/
```
