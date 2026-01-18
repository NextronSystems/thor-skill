#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2:
    print("Usage: summarize_thor_log.py <logfile>", file=sys.stderr)
    sys.exit(2)

logfile = sys.argv[1]
if not os.path.exists(logfile):
    print(f"Error: file not found: {logfile}", file=sys.stderr)
    sys.exit(2)

print("TODO: implement")
sys.exit(0)
