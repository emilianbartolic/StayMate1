"""Explicit development adapter for the installed Codex CLI.

The FastAPI runtime also invokes Codex separately in an ephemeral, read-only
mode when no OpenAI key is configured. This adapter remains the explicit
builder/reviewer entry point; workspace writes require --allow-write.
"""
import argparse
import subprocess
from pathlib import Path

def run_codex(prompt: str, workspace: str, allow_write: bool = False) -> int:
    root = str(Path(workspace).resolve())
    command = ["codex", "exec", "-C", root, "--sandbox", "workspace-write" if allow_write else "read-only", "--ask-for-approval", "on-request", prompt]
    return subprocess.call(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StayMate Codex development adapter")
    parser.add_argument("prompt")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--allow-write", action="store_true", help="requires explicit human approval before generated edits")
    args = parser.parse_args()
    raise SystemExit(run_codex(args.prompt, args.workspace, args.allow_write))
