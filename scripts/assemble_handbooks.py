#!/usr/bin/env python3
"""Assemble Pandoc manuscripts for the notes hub and five mini-books.

Chapter prose stays under notes/. Each mini-book is a GitBook root at
books/<slug>/ (README.md, SUMMARY.md, book.json). Generated introductions
use Australian English and avoid em dashes.

Usage:
  python3 scripts/assemble_handbooks.py BUILD_DIR
  python3 scripts/assemble_handbooks.py --verify
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

AUTHOR = "Musfira Jamil"
ORIGIN = "These chapters started as learning notes and primers."

# Published order and URL slugs. Directory names under books/ match these.
EXPECTED = (
    "genomics",
    "databricks",
    "software-engineering",
    "statistics",
    "data-generation",
)

# SUMMARY links (except the book README) must stay inside these trees.
# Paths are relative to books/<slug>/.
ALLOWED_PREFIXES = {
    "genomics": (
        "../../notes/genomics/",
        "../../notes/interactive-tutorials/",
    ),
    "databricks": ("../../notes/databricks-series/",),
    "software-engineering": ("../../notes/software-engineering/",),
    "statistics": ("../../notes/statistics/",),
    "data-generation": ("../../notes/data-generation-techniques/",),
}

HUB_TITLE = "Technical Notes"
HUB_SUBTITLE = "Five short handbooks of learning notes and primers"
HUB_INTRO = (
    "Welcome. This library publishes practical technical notes as five short "
    "handbooks, covering genomics, Databricks, software engineering for "
    "bioinformatics, statistics, and laboratory data generation. They started "
    "as learning notes and primers.\n\n"
    "Each handbook stands on its own, with its own table of contents. "
    "Choose one below.\n"
)

LINK_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H1_RE = re.compile(r"^#\s+\S")
EM_DASH = "\u2014"
EN_DASH = "\u2013"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            rest = text[end + 4 :]
            if rest.startswith("\n"):
                rest = rest[1:]
            return rest
    return text


def first_paragraph(markdown: str) -> str:
    """First prose paragraph, skipping a leading H1."""
    lines = markdown.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index < len(lines) and H1_RE.match(lines[index]) and not lines[index].startswith("##"):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    buffer: list[str] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.startswith("#"):
            break
        buffer.append(line.strip())
        index += 1
    return " ".join(buffer).strip()


def parse_summary(text: str):
    for line in text.splitlines():
        if H1_RE.match(line) and not line.startswith("##"):
            continue
        heading = H2_RE.match(line)
        if heading:
            yield ("heading", heading.group(1).strip())
            continue
        link = LINK_RE.match(line)
        if link:
            yield ("link", link.group(1).strip(), link.group(2).strip())


def require_str(meta: dict, key: str, path: Path) -> str:
    value = meta.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{path} is missing a non-empty string '{key}'")
    return value.strip()


def display(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def has_href(html: str, href: str) -> bool:
    return re.search(r'href\s*=\s*"' + re.escape(href) + r'"', html) is not None


def load_book(root: Path, slug: str) -> dict:
    book_dir = root / "books" / slug
    meta_path = book_dir / "book.json"
    if not meta_path.is_file():
        raise SystemExit(f"Missing {display(meta_path, root)}")
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {display(meta_path, root)}: {exc}") from exc
    if not isinstance(meta, dict):
        raise SystemExit(f"{display(meta_path, root)} must be a JSON object")

    structure = meta.get("structure") or {}
    if not isinstance(structure, dict):
        raise SystemExit(f"{display(meta_path, root)} structure must be an object")
    readme_name = structure.get("readme") or "README.md"
    summary_name = structure.get("summary") or "SUMMARY.md"
    readme_path = book_dir / readme_name
    summary_path = book_dir / summary_name
    for path in (readme_path, summary_path):
        if not path.is_file():
            raise SystemExit(f"Missing {display(path, root)}")

    title = require_str(meta, "title", meta_path)
    subtitle = require_str(meta, "subtitle", meta_path)
    blurb = first_paragraph(readme_path.read_text(encoding="utf-8"))
    if not blurb:
        raise SystemExit(f"{display(readme_path, root)} needs an introductory paragraph")

    allowed = ALLOWED_PREFIXES[slug]
    chapters: list[tuple[str, Path]] = []
    seen_prefixes: set[str] = set()
    parts: list[str] = []
    for kind, *payload in parse_summary(summary_path.read_text(encoding="utf-8")):
        if kind == "heading":
            parts.append(f"# {payload[0]}\n\n")
            continue
        link_title, rel = payload
        if Path(rel).name == "README.md":
            continue
        normalised = rel.replace("\\", "/")
        matched = next((prefix for prefix in allowed if normalised.startswith(prefix)), None)
        if matched is None:
            allowed_text = ", ".join(allowed)
            raise SystemExit(
                f"{display(summary_path, root)} link {rel!r} is outside this "
                f"book's sources ({allowed_text})"
            )
        seen_prefixes.add(matched)
        note_path = (summary_path.parent / rel).resolve()
        try:
            note_path.relative_to(root.resolve())
        except ValueError:
            raise SystemExit(f"Link escapes the repository: {rel}")
        if not note_path.is_file():
            raise SystemExit(
                f"Missing note {rel} referenced from {display(summary_path, root)}"
            )
        body = strip_frontmatter(note_path.read_text(encoding="utf-8")).strip()
        if not body:
            raise SystemExit(f"Empty note {display(note_path, root)}")
        parts.append(body + "\n\n")
        chapters.append((link_title, note_path))

    missing_prefixes = [prefix for prefix in allowed if prefix not in seen_prefixes]
    if missing_prefixes:
        raise SystemExit(
            f"{display(summary_path, root)} does not link into: "
            + ", ".join(missing_prefixes)
        )
    if not chapters:
        raise SystemExit(f"No chapters in {display(summary_path, root)}")

    return {
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "blurb": blurb,
        "chapters": chapters,
        "body": "".join(parts),
    }


def manuscript(title: str, subtitle: str, body: str, today: str) -> str:
    return (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"subtitle: {yaml_quote(subtitle)}\n"
        f"author: {yaml_quote(AUTHOR)}\n"
        f"date: {yaml_quote(today)}\n"
        "---\n\n"
        f"{body.rstrip()}\n"
    )


def book_intro(blurb: str) -> str:
    return (
        f"{blurb}\n\n"
        f"{ORIGIN}\n\n"
        "[Notes library](../index.html){.handbook-link}\n\n"
    )


def ensure_layout(root: Path) -> None:
    books_root = root / "books"
    if not books_root.is_dir():
        raise SystemExit("Missing books/ directory")
    found = {path.name for path in books_root.iterdir() if path.is_dir()}
    expected = set(EXPECTED)
    if found != expected:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise SystemExit(
            "books/ must contain exactly the five mini-books (" + "; ".join(details) + ")"
        )


def assemble(root: Path, build_dir: Path) -> None:
    ensure_layout(root)

    today = date.today().isoformat()
    books = [load_book(root, slug) for slug in EXPECTED]
    hub_parts = [HUB_INTRO.rstrip() + "\n\n"]
    manifest = []
    for book in books:
        slug = book["slug"]
        intro = book_intro(book["blurb"])
        text = manuscript(book["title"], book["subtitle"], intro + book["body"], today)
        (build_dir / f"{slug}.md").write_text(text, encoding="utf-8")
        manifest.append(f"{slug}\t{book['title']}")
        hub_parts.append(f"# {book['title']}\n\n")
        hub_parts.append(f"{book['blurb']}\n\n")
        hub_parts.append(
            f"[Open {book['title']}]({slug}/){{.handbook-link}}\n\n"
        )
        print(f"Assembled {slug}: {len(book['chapters'])} chapters")

    hub = manuscript(HUB_TITLE, HUB_SUBTITLE, "".join(hub_parts), today)
    (build_dir / "hub.md").write_text(hub, encoding="utf-8")
    (build_dir / "books.tsv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    reject_dashes(hub, "hub manuscript")
    print(f"Assembled hub: {len(books)} handbooks")


def reject_dashes(text: str, label: str) -> None:
    if EM_DASH in text or EN_DASH in text:
        raise SystemExit(f"{label} contains an em dash or en dash")


def verify(root: Path) -> None:
    ensure_layout(root)
    problems: list[str] = []
    docs = root / "docs"
    styles = docs / "styles.css"
    if not (docs / ".nojekyll").is_file():
        problems.append("missing docs/.nojekyll")
    if not styles.is_file():
        problems.append("missing docs/styles.css")
    else:
        css = styles.read_text(encoding="utf-8")
        if "--paper:" not in css or "handbook-link" not in css:
            problems.append("docs/styles.css is missing the shared handbook theme")

    hub_path = docs / "index.html"
    if not hub_path.is_file():
        raise SystemExit("Missing docs/index.html")
    hub = hub_path.read_text(encoding="utf-8")
    hub_flat = squash(hub)
    reject_dashes(hub, "docs/index.html")

    if not has_href(hub, "styles.css"):
        problems.append("hub is missing href=\"styles.css\"")
    if has_href(hub, "../styles.css") or re.search(r'href\s*=\s*"/(?:notes/)?styles\.css"', hub):
        problems.append("hub stylesheet link is not relative to /notes/")
    if 'id="TOC"' not in hub or 'lang="en-AU"' not in hub:
        problems.append("hub is missing the table of contents or en-AU language")
    if "learning notes and primers" not in hub_flat:
        problems.append("hub should say the notes started as learning notes and primers")
    if hub.count("handbook-link") < len(EXPECTED):
        problems.append("hub should link each mini-book")

    title_owner: dict[str, str] = {}
    html_by_slug: dict[str, str] = {}
    for slug in EXPECTED:
        book = load_book(root, slug)
        html_path = docs / slug / "index.html"
        if not html_path.is_file():
            problems.append(f"missing docs/{slug}/index.html")
            continue
        html = html_path.read_text(encoding="utf-8")
        html_by_slug[slug] = html
        flat = squash(html)
        if not has_href(html, "../styles.css"):
            problems.append(f"{slug} is missing href=\"../styles.css\"")
        if has_href(html, "styles.css") or re.search(
            r'href\s*=\s*"/(?:notes/)?styles\.css"', html
        ):
            problems.append(f"{slug} stylesheet would not resolve under /notes/{slug}/")
        if not has_href(html, "../index.html"):
            problems.append(f"{slug} is missing the link back to the notes library")
        if 'id="TOC"' not in html or 'lang="en-AU"' not in html:
            problems.append(f"{slug} is missing the table of contents or en-AU language")
        if "handbook-link" not in html:
            problems.append(f"{slug} is missing the notes library link style")
        if book["title"] not in flat:
            problems.append(f"{slug} is missing its title")
        if ORIGIN not in flat:
            problems.append(f"{slug} should say the chapters started as learning notes and primers")
        if book["blurb"] not in flat:
            problems.append(f"{slug} is missing its introduction")
        if not has_href(hub, f"{slug}/"):
            problems.append(f"hub is missing a link to {slug}/")
        if book["title"] not in hub_flat:
            problems.append(f"hub is missing the {book['title']} handbook")
        for chapter_title, _path in book["chapters"]:
            if chapter_title in title_owner:
                problems.append(f"duplicate chapter title: {chapter_title}")
            title_owner[chapter_title] = slug
            if squash(chapter_title) not in flat:
                problems.append(f"{slug} is missing chapter {chapter_title!r}")
            if len(chapter_title) >= 12 and squash(chapter_title) not in squash(book["blurb"]):
                if squash(chapter_title) in hub_flat:
                    problems.append(f"hub includes chapter prose or title {chapter_title!r}")

    for chapter_title, owner in title_owner.items():
        flat_title = squash(chapter_title)
        found = [slug for slug, html in html_by_slug.items() if flat_title in squash(html)]
        if found != [owner]:
            problems.append(
                f"chapter {chapter_title!r} appears in {found or 'no handbook'}, expected {owner}"
            )

    if problems:
        raise SystemExit("Handbook verification failed:\n  " + "\n  ".join(problems))
    print("Verified hub, five handbooks, stylesheet links, and chapter placement")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    if len(sys.argv) == 2 and sys.argv[1] == "--verify":
        verify(root)
        return
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: assemble_handbooks.py BUILD_DIR | assemble_handbooks.py --verify"
        )
    build_dir = Path(sys.argv[1])
    build_dir.mkdir(parents=True, exist_ok=True)
    assemble(root, build_dir)


if __name__ == "__main__":
    main()
