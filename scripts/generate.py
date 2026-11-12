#!/usr/bin/env python3
"""Write themes/kanagawa-<variant> from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

# zathura option -> palette role.
OPTIONS = {
    "default-bg": "ui.bg",
    "default-fg": "ui.fg",
    "statusbar-bg": "ui.bg_m3",
    "statusbar-fg": "ui.fg_dim",
    "inputbar-bg": "ui.bg_m3",
    "inputbar-fg": "ui.fg",
    "notification-bg": "ui.bg_m3",
    "notification-fg": "ui.fg",
    "notification-error-bg": "diag.error",
    "notification-error-fg": "ui.bg",
    "notification-warning-bg": "diag.warning",
    "notification-warning-fg": "term.black",
    "completion-bg": "ui.pmenu.bg",
    "completion-fg": "ui.pmenu.fg",
    "completion-group-bg": "ui.bg_p1",
    "completion-group-fg": "ui.fg_dim",
    "completion-highlight-bg": "ui.pmenu.bg_sel",
    "completion-highlight-fg": "ui.pmenu.fg",
    "index-bg": "ui.bg",
    "index-fg": "ui.fg",
    "index-active-bg": "ui.bg_visual",
    "index-active-fg": "ui.fg",
    "render-loading-bg": "ui.bg",
    "render-loading-fg": "ui.fg_dim",
    "recolor-lightcolor": "ui.bg",
    "recolor-darkcolor": "ui.fg",
}
# Search matches are drawn over the page, so they are half transparent.
HIGHLIGHTS = {"highlight-color": "ui.bg_search", "highlight-active-color": "diag.warning"}


def rgba(h, alpha):
    return f"rgba({int(h[1:3], 16)},{int(h[3:5], 16)},{int(h[5:7], 16)},{alpha})"


def theme(variant, colors):
    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/zathura", ""]
    out += [f'set {k:<24} "{colors[r]}"' for k, r in OPTIONS.items()]
    out += [f'set {k:<24} "{rgba(colors[r], 0.5)}"' for k, r in HIGHLIGHTS.items()]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
