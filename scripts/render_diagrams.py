"""Render every .mmd file in docs/diagrams/ to a sibling .png.

Uses the mermaid.ink public API so no local Node.js / mermaid-cli is required.

Usage (from repo root):
    python scripts/render_diagrams.py
    python scripts/render_diagrams.py --dir docs/diagrams
"""

from __future__ import annotations

import argparse
import base64
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path


def _pako_encode(mermaid: str) -> str:
    """Mermaid.ink `pako:` format — deflated + urlsafe base64. Survives large payloads."""
    data = {"code": mermaid, "mermaid": {"theme": "default"}}
    import json

    raw = json.dumps(data).encode("utf-8")
    compressed = zlib.compress(raw, 9)
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def render(src: Path, dst: Path) -> None:
    mermaid = src.read_text(encoding="utf-8")
    encoded = _pako_encode(mermaid)
    url = f"https://mermaid.ink/img/pako:{encoded}?type=png&bgColor=!white"
    print(f"  rendering {src.name} -> {dst.name}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (render_diagrams.py)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"    HTTP {e.code} from mermaid.ink: {e.read().decode('utf-8', 'ignore')}\n")
        raise
    dst.write_bytes(body)
    print(f"    saved {len(body)} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("docs/diagrams"),
        help="directory containing .mmd files (default: docs/diagrams)",
    )
    args = parser.parse_args()

    diagrams_dir: Path = args.dir
    if not diagrams_dir.is_dir():
        sys.stderr.write(f"error: {diagrams_dir} is not a directory\n")
        sys.exit(1)

    sources = sorted(diagrams_dir.glob("*.mmd"))
    if not sources:
        sys.stderr.write(f"warning: no .mmd files in {diagrams_dir}\n")
        return

    print(f"rendering {len(sources)} diagram(s) from {diagrams_dir}/")
    failures = 0
    for src in sources:
        dst = src.with_suffix(".png")
        try:
            render(src, dst)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"  FAILED {src.name}: {e}\n")
            failures += 1
    if failures:
        sys.exit(1)
    print("done.")


if __name__ == "__main__":
    main()
