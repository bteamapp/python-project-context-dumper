# Free Python Project Context Dumper

A tiny Python tool that recursively scans a project folder and creates a single Markdown file (`project_context.md`) containing all **text-based files** — skipping images, videos, audio files, and itself.

Perfect for passing full project context into an AI (LLM) for summarization, agent memory, or fine-tuning tasks.

---

## ✅ Features

- ✅ Recursively scans current directory and all subdirectories
- ✅ Skips media files (images, video, audio)
- ✅ Skips itself and its generated output
- ✅ Outputs a clean, Markdown-formatted `.md` file with relative paths and contents

---

## 🚀 Usage

1. Clone or copy this script into the root of your project:

```bash
wget https://raw.githubusercontent.com/yourname/project-context-dumper/main/context_dumper.py
