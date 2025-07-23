#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Project Context Dumper
Author: bTeam App
License: GPLv3
Description:
    Recursively scan all text-based files in the current directory and subdirectories.
    Skips images, video, audio, and itself. Outputs a single Markdown file
    (`project_context.md`) with all content and paths for LLM/AI context loading.
"""

import os
from pathlib import Path
import mimetypes
from datetime import datetime

# File types to skip based on MIME type
SKIP_MIME_PREFIXES = ('image', 'video', 'audio')

# Define paths
BASE_DIR = Path(__file__).resolve().parent
SCRIPT_FILE = Path(__file__).resolve()
OUTPUT_FILE = BASE_DIR / 'project_context.md'

def should_skip(file_path: Path) -> bool:
    if file_path.resolve() in [SCRIPT_FILE, OUTPUT_FILE]:
        return True
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.startswith(SKIP_MIME_PREFIXES)
    return False

def read_text_file(path: Path) -> str | None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ Could not read: {path} ({e})")
        return None

def collect_text_files(base_dir: Path):
    collected = []
    for path in base_dir.rglob('*'):
        if path.is_file() and not should_skip(path):
            content = read_text_file(path)
            if content:
                relative_path = path.relative_to(base_dir)
                collected.append((relative_path, content))
    return collected

def write_to_markdown(collected_files: list[tuple[Path, str]], output_path: Path):
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("# bTeam App: Project Context Dump\n\n")
        out.write(f"> **Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write("> Auto-generated for AI/Large Language Model context ingestion.\n\n")
        for rel_path, content in collected_files:
            out.write(f"\n## File: `{rel_path}`\n\n")
            out.write("```text\n")
            out.write(content)
            out.write("\n```\n")

if __name__ == '__main__':
    print(f"🔍 Scanning directory: {BASE_DIR}")
    files = collect_text_files(BASE_DIR)
    write_to_markdown(files, OUTPUT_FILE)
    print(f"✅ Context file written to: {OUTPUT_FILE} ({len(files)} files included)")


input('Enter to continue...')
