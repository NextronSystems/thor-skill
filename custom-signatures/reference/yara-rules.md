---
name: yara-rules
description: THOR YARA rule types, filename-based initialization, and THOR-specific enhancements.
---

# YARA Rules in THOR

THOR allows you to include your own custom YARA rules. Rules must have:
- `.yar` extension for plain text YARA rules
- `.yas` extension for encrypted YARA rules (encrypted using `thor-util`)

Custom YARA rules must be saved to the `.\custom-signatures\yara` folder.

To apply only custom YARA rules and IOCs, use the `--custom-signatures-only` flag.

## YARA Rule Types

There are **three YARA rule types** that you can define in THOR:

1. **Generic rules** (subtype: Process rules)
2. **Meta rules**
3. **Keyword rules** (subtypes: Registry rules, Log rules)

### Rule Type Determination by Filename

The rule type is determined by **specific keywords within the filename**:

| Filename Contains | Rule Type |
|-------------------|-----------|
| `meta` | Meta rules |
| `keyword`, `registry`, or `log` | Keyword rules (with specified subtype if applicable) |
| `process`, or **none** of the keywords above | Generic rules (with process subtype if specified) |

### Filename Examples

| Filename | Rule Type |
|----------|-----------|
| `incident-feb17.yar` | Generic rule |
| `event-log-rules.yar` | Log rule (keyword subtype) |
| `custom-meta.yar` | Meta rule |
| `incident-feb17-registry.yar` | Registry rule (keyword subtype) |
| `case-a23-process-rules.yar` | Process rule (generic subtype) |
| `redkitten-tasks-keyword.yar` | Keyword rule |

---

## Generic YARA Rules

Generic YARA rules are applied to:

- **Files**: All files smaller than `--file-size-limit` that have been matched by [Deepscan Rules](#deepscan-rules)
- **Process memory**: All processes with working set memory size smaller than `--process-size-limit`
- **DeepDive data chunks**: Data chunks read during DeepDive scan

### Process Subtype

Rules with the `process` subtype (filename contains `process`) are **only applied to process memory and DeepDive chunks**, not to files.

### Important Notes

- Only files actively selected by [Deepscan Rules](#deepscan-rules) are scanned with generic YARA rules
- [Additional Attributes](#additional-attributes) are available based on the scanned object:
  - For files: based on the file itself
  - For process memory: based on the process's image
  - For data chunks: based on the file where the chunk originates

---

## Meta YARA Rules

Meta rules are applied to **all files without exception**.

However, they can only access:
- The [Additional Attributes](#additional-attributes)
- The **first 64KB** of the file

### Special File Types

Meta rules are also applied to irregular files. The bytes scanned are provided by THOR:

- **Symlinks**: File content is their target path
- **Directories**: File content is the directory listing (file names separated by newlines)

### Use Cases

Meta rules are most commonly used to:
- Trigger other features (see Feature Selectors)
- Choose a file for scanning with Generic Rules (via Deepscan Rules)

### Deepscan Rules

If a meta rule with the special tag `DEEPSCAN` matches a file, THOR will scan the file with [Generic YARA Rules](#generic-yara-rules).

THOR's signatures already contain deepscan rules for common file types used by attackers. These rules are used even with `--custom-signatures-only`.

**FORCE Tag**: If a deepscan rule has the `FORCE` tag, it ignores the file size limit and always triggers a scan with generic YARA rules. Use with care — this can massively increase scan times.

---

## Keyword YARA Rules

Keyword rules are applied to **all objects that are checked** by THOR modules.

### Subtypes

| Subtype | Filename Contains | Applied To |
|---------|-------------------|------------|
| Registry | `registry` | Registry keys/values only |
| Log | `log` | Log lines, event log entries, journald entries |
| (none) | `keyword` | All module output strings |

### Keyword Rule Scanning

Keyword rule scanning (including registry and logs) uses [Bulk Scanning](#bulk-scanning) for performance.

### Registry YARA Rules

THOR composes a string from registry key values in this format:

```
KEYPATH;VALUENAME;VALUE\n
KEYPATH;VALUENAME;VALUE\n
...
```

**Important:** Registry base names (HKEY_LOCAL_MACHINE, HKLM, HKCU, HKEY_CURRENT_CONFIG) are **NOT** part of the key path. They depend on the analyzed hive and should not be in your rule strings.

**Value formatting:**

| Registry Type | Format |
|---------------|--------|
| REG_BINARY | Hex encoded, uppercase |
| REG_MULTI_SZ | Multiple strings separated by `\0` |
| REG_DWORD | Decimal (e.g., `32` for 0x00000020) |
| String values | Printed normally |

**Example Registry Rule:**

```yara
rule Registry_DarkComet {
    meta:
        description = "DarkComet Registry Keys"
    strings:
        $a1 = "LEGACY_MY_DRIVERLINKNAME_TEST;NextInstance"
        $a2 = "\\Microsoft\\Windows\\CurrentVersion\\Run;MicroUpdate"
        $a3 = "Path;Value;4D5A00000001"                          // REG_BINARY
        $a4 = "Shell\\Open;Command;explorer.exe\\0comet.exe"     // REG_MULTI_SZ
        $a5 = ";Type;32"                                         // REG_DWORD 0x20
    condition:
        1 of them
}
```

Remember: Use `registry` in the filename (e.g., `registry_exe_in_value.yar`) to initialize as registry rules.

### Log YARA Rules

YARA rules for logs are applied as follows:

- **Text logs**: Each line is passed to the YARA rules
- **Windows Event Logs**: Each event is serialized as: `Key1: Value1  Key2: Value2  ...`
  - Each key/value pair is an entry in EventData or UserData in the XML representation

---

## Score Attribute

The [score](scores.html#scoring) of a YARA rule can be specified as a meta attribute:

```yara
rule demo_rule_score {
    meta:
        description = "Demo Rule"
        score = 80          // Default is 75 if not specified
    strings:
        $a1 = "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
        $a2 = "honkers" fullword
    condition:
        1 of them
}
```

The scoring system allows including ambiguous, low-scoring rules that would generate too many false positives in other scanners.

---

## Additional Attributes (External Variables)

THOR provides external variables in generic and meta YARA rules:

| Variable | Description | Example |
|----------|-------------|---------|
| `filename` | Single file name | `cmd.exe` |
| `filepath` | File path without filename | `C:\temp` |
| `extension` | File extension with leading `.`, lowercase | `.exe` |
| `filetype` | File type based on magic header | `EXE`, `ZIP` |
| `filesize` | File size in bytes (YARA built-in) | 1024 |
| `timezone` | System's timezone | `CET` |
| `language` | System language settings | `en-US` |
| `owner` | File owner | `NT-AUTHORITY\SYSTEM` (Windows), `root` (Linux) |
| `group` | File group | `root` (Linux), empty on Windows |
| `filemode` | POSIX-style file mode | Artificial on Windows |
| `osversion` | Windows build number | `19045` (0 on non-Windows) |
| `unpack_parent` | Immediate origin | `ZIP`, `EMAIL`, `CHM`, etc. |
| `unpack_source` | Full origin chain | `EMAIL>ZIP` |
| `permissions` | File permissions | Unix: mode string, Windows: DACL |
| `age` | File age in days | Based on creation timestamp |

### Example Rules with External Variables

```yara
rule demo_rule_enhanced {
    meta:
        description = "Demo Rule - Eicar"
    strings:
        $a1 = "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
    condition:
        $a1 and filename matches /eicar\.com/
}
```

More complex rule:

```yara
rule demo_rule_complex {
    meta:
        author = "F.Roth"
    strings:
        $a1 = "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
    condition:
        $a1 
        and filename matches /eicar\.(com|dll|exe)/ 
        and filesize < 100
}
```

Real-world example:

```yara
rule HvS_Client_2_APT_Java_IDX_Content_hard {
    meta:
        description = "VNCViewer.jar Entry in Java IDX file"
    strings:
        $a1 = "vncviewer.jar"
        $a2 = "vncviewer/VNCViewer.class"
    condition:
        1 of ($a*) and extension matches /\.idx/
}
```

---

## Restricting YARA Rule Matches

Use the `limit` meta attribute to restrict rules to specific modules:

```yara
rule Malware_in_fileobject {
    meta:
        description = "Think Tank Campaign"
        limit = "Filescan"          // Only apply in Filescan module
    strings:
        $s1 = "evilstring-infile-only"
    condition:
        1 of them
}
```

See [Modules](../scanning/modules.html) and [Features](../scanning/features.html) for all available components.

### Limit Attribute Examples

```yara
meta:
    limit = "Mutex"           // Only in Mutex module
    limit = "ServiceCheck"    // Only in ServiceCheck module
    limit = "ScheduledTasks"  // Only in ScheduledTasks module
    limit = "Filescan"        // Only for file objects
```

---

## Bulk Scanning

THOR scans objects (registry values, log lines, etc.) in **bulks** to reduce YARA invocation overhead.

**How it works:**

1. THOR gathers objects that need scanning
2. When enough entries are gathered, they're combined (separated by line breaks) and passed to YARA
3. The ruleset is modified to remove false positive conditions — otherwise, FP strings in one entry could prevent detection in another
4. If any rule matches, the specific entries containing match strings are re-scanned individually to confirm

---

## Rule Placement Summary

```
thor/
└── custom-signatures/
    └── yara/
        ├── incident-feb17.yar              # Generic rules
        ├── case-a23-process-rules.yar      # Process rules (memory only)
        ├── custom-meta.yar                 # Meta rules (all files, 64KB)
        ├── redkitten-tasks-keyword.yar     # Keyword rules (module output)
        ├── incident-registry.yar           # Registry rules
        └── event-log-rules.yar             # Log rules
```

---

## Best Practices

### Creating YARA Rules

1. **Extract information** from malware samples (strings, bytecode, MD5)
2. **Create rule file** with:
   - Unique rule name (duplicates cause errors)
   - Clear description
   - Appropriate score (optional, default 75)
3. **Test with YARA binary** before deploying to THOR:
   - Verify positive match on malware
   - Check for false positives on Windows/Program Files
4. **Copy to THOR** and verify no errors on startup

### Performance Guidelines

- Avoid regex with undefined length (`.*`, `.+`, `\w+`)
- Use `fullword` modifier when possible
- Prefer literal strings over regex
- Test rules with `yara` binary before deploying
- Use `score = 0` for detection-only rules

### Typical Pitfalls

**Problematic regex:**
```yara
// BAD - causes YARA to loop on certain files
$gif1 = /\w+\.gif/

// GOOD - bounded regex
$gif1 = /[a-zA-Z0-9_]{1,20}\.gif/
```

**Duplicate rule names** cause THOR initialization to fail.

### Useful Resources

- [yarGen](https://github.com/Neo23x0/yarGen) - YARA rule generator
- [YARA Performance Guidelines](https://gist.github.com/Neo23x0/e3d4e316d7441d9143c7)
- [Write Simple Sound YARA Rules](https://www.nextron-systems.com/2015/02/16/write-simple-sound-yara-rules/)
- [Write Simple Sound YARA Rules Part 2](https://www.nextron-systems.com/2015/10/17/how-to-write-simple-but-sound-yara-rules-part-2/)

---

## Encryption

To protect sensitive rules:

```bash
thor-util encrypt --file my-rules.yar
# Creates my-rules.yas
```

| Plain | Encrypted |
|-------|-----------|
| `.yar` | `.yas` |
| `.txt` | `.dat` |
| `.yml` | `.yms` |
| `.json` | `.jsos` |
