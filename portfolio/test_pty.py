#!/usr/bin/env python3
"""Simple test script to verify PTY output."""
import sys
import time

print("Hello from PTY test!")
print(f"stdin.isatty(): {sys.stdin.isatty()}")
print(f"stdout.isatty(): {sys.stdout.isatty()}")
sys.stdout.flush()

# Wait for input
print("Press Enter to exit...")
sys.stdout.flush()
try:
    input()
except EOFError:
    print("Got EOF")
print("Goodbye!")
