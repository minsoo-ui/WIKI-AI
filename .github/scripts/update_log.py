from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os


LOG_PATH = Path("docs/UPDATE_LOG.md")


def _short_sha(value: str | None) -> str:
    if not value:
        return "unknown"
    return value[:7]


def main() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Update Log\n\n", encoding="utf-8")

    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    actor = os.getenv("GITHUB_ACTOR", "unknown")
    branch = os.getenv("GITHUB_REF_NAME", "unknown")
    sha = _short_sha(os.getenv("GITHUB_SHA"))
    workflow = os.getenv("GITHUB_WORKFLOW", "unknown")
    run_url = (
        f"https://github.com/{os.getenv('GITHUB_REPOSITORY', '')}/actions/runs/"
        f"{os.getenv('GITHUB_RUN_ID', '')}"
    )

    new_entry = (
        f"- {run_time} | actor: `{actor}` | branch: `{branch}` | sha: `{sha}` "
        f"| workflow: `{workflow}` | run: {run_url}\n"
    )

    content = LOG_PATH.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    if not lines:
        lines = ["# Update Log\n", "\n"]
    elif lines[0].strip() != "# Update Log":
        lines.insert(0, "# Update Log\n")
        if len(lines) == 1 or lines[1].strip():
            lines.insert(1, "\n")

    body = "".join(lines[2:]) if len(lines) >= 2 else ""
    LOG_PATH.write_text("# Update Log\n\n" + new_entry + body, encoding="utf-8")


if __name__ == "__main__":
    main()
