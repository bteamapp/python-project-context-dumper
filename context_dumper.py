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

print("For Python 3.10+ only")
print("Open source at https://github.com/bteamapp/python-project-context-dumper\n")


# MIME types to skip
SKIP_MIME_PREFIXES = ('image', 'video', 'audio')

# List of filenames/folders to skip (can be customized)
SKIP_PATHS = {
    '.git',
    '.gitignore',
    'node_modules',
    '__pycache__',
    '.DS_Store',
    # add more files/folders if needed
}

# Root directory path (where this .py script is located)
BASE_DIR = Path(__file__).resolve().parent
SCRIPT_FILE = Path(__file__).resolve()
OUTPUT_FILE = BASE_DIR / 'project_context.md'


def should_skip(file_path: Path) -> bool:
    # Skip the running script file and output file
    if file_path.resolve() == SCRIPT_FILE or file_path.resolve() == OUTPUT_FILE:
        return True

    # Skip if any part of the path matches names in SKIP_PATHS
    for part in file_path.parts:
        if part in SKIP_PATHS:
            return True

    # Skip by MIME type (image, video, audio)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.startswith(SKIP_MIME_PREFIXES)
    return False


def read_text_file(path: Path) -> str | None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ Cannot read: {path} ({e})")
        return None


def collect_text_files(base_dir: Path):
    collected = []

    for path in base_dir.rglob('*'):
        try:
            if path.is_file() and not should_skip(path):
                content = read_text_file(path)
                if content:
                    relative_path = path.relative_to(base_dir)
                    collected.append((relative_path, content))
        except OSError as e:
            print(f"⚠️ Bỏ qua: {path} (lỗi hệ thống: {e})")
        except Exception as e:
            print(f"⚠️ Bỏ qua: {path} (lỗi không xác định: {e})")

    return collected



def write_to_markdown(collected_files: list[tuple[Path, str]], output_path: Path):
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("# Project Context Dump\n\n")
        out.write(f"> Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write("> Automatically generated by script so AI can understand the entire structure and content.\n\n")

        for rel_path, content in collected_files:
            out.write(f"\n## ·  `{rel_path}`\n\n")
            out.write("```text\n")
            out.write(content)
            out.write("\n```\n")


if __name__ == '__main__':
    print(f"🔍 Collecting files from: {BASE_DIR}")
    files = collect_text_files(BASE_DIR)
    write_to_markdown(files, OUTPUT_FILE)
    print(f"✅ Created context file: {OUTPUT_FILE} ({len(files)} files)")

    input('Press any key to exit')

input('Enter to continue...')
