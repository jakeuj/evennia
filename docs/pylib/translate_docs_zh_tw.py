"""Batch-translate Evennia docs to Traditional Chinese.

This helper translates reader-facing Markdown docs under ``docs/source`` while
preserving the MyST/Markdown structure used by the documentation site.

The script is intentionally conservative:

- It skips ``docs/source/api`` and files that already contain CJK text.
- It preserves code fences, reference definitions, special link targets, and
  most code-like identifiers.
- It adds explicit MyST anchors before translated headings so existing
  ``#fragment`` links keep working after headings are localized.

The translation engine uses ``deep-translator`` and the final text is passed
through OpenCC to normalize to Traditional Chinese.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError as exc:  # pragma: no cover - import guard for CLI usage
    raise SystemExit(
        "deep-translator is required. Install it with `uv pip install deep-translator`."
    ) from exc

try:
    from opencc import OpenCC
except ImportError as exc:  # pragma: no cover - import guard for CLI usage
    raise SystemExit(
        "opencc-python-reimplemented is required. Install it with "
        "`uv pip install opencc-python-reimplemented`."
    ) from exc


DOCS_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = DOCS_ROOT / "source"
API_ROOT = SOURCE_ROOT / "api"
CACHE_PATH = DOCS_ROOT / ".cache" / "translate_docs_zh_tw.json"

TRANSLATE_DIRECTIVES = {
    "admonition",
    "attention",
    "caution",
    "danger",
    "error",
    "hint",
    "important",
    "note",
    "sidebar",
    "tip",
    "warning",
}
PRESERVE_DIRECTIVES = {
    "code-block",
    "csv-table",
    "eval-rst",
    "figure",
    "image",
    "list-table",
    "literalinclude",
    "math",
    "mermaid",
    "parsed-literal",
    "pull-quote",
    "rubric",
    "seealso",
    "table",
    "toctree",
}

GLOSSARY_TERMS = [
    "Attribute",
    "AttributeProperty",
    "CmdSet",
    "CmdSets",
    "Contrib",
    "Contribs",
    "EvAdventure",
    "Evennia",
    "EvEditor",
    "EvForm",
    "EvMenu",
    "EvMore",
    "EvTable",
    "GMCP",
    "Lock",
    "LockFunc",
    "LockFuncs",
    "NAttribute",
    "NAttributes",
    "OOB",
    "Portal",
    "Script",
    "Scripts",
    "Session",
    "Sessions",
    "Tag",
    "Tags",
    "Typeclass",
    "Typeclasses",
    "webclient",
    "webserver",
]

EXACT_TRANSLATIONS = {
    "Access": "存取控制",
    "Base components": "基礎元件",
    "Beginner Tutorial": "新手教學",
    "Coding and development help": "開發與程式撰寫",
    "Configuration": "設定",
    "Core Components": "核心元件",
    "Core Concepts": "核心概念",
    "Deep Dives": "深入主題",
    "Evennia Changelog": "Evennia 變更紀錄",
    "Extending the Server": "擴充伺服器",
    "General concepts": "一般概念",
    "Going Online": "上線",
    "How-To's": "Howto",
    "Old Tutorials": "較舊的教學",
    "Server Setup and Life": "伺服器設定與生命週期",
    "Systems": "系統",
    "Text processing": "文字處理",
    "This sums up all steps of maintaining your Evennia game from first installation to production release.": (
        "這裡整理了 Evennia 遊戲從第一次安裝到正式上線的整體維運流程。"
    ),
    "Tutorials and How-To's": "教學與 Howto",
    "Utils and tools": "工具與實用模組",
    "Web components": "Web 元件",
    "Website Tutorials": "網站教學",
}

POST_TRANSLATION_REPLACEMENTS = {
    "上網": "上線",
    "配置": "設定",
    "教程": "教學",
    "命令": "指令",
    "客戶端": "用戶端",
    "字符": "字元",
    "鏈接": "連結",
    "運行": "執行",
    "數據": "資料",
    "程序": "程式",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BULLET_RE = re.compile(r"^(\s*[-*+]\s+)(.+?)\s*$")
NUMBERED_RE = re.compile(r"^(\s*\d+\.\s+)(.+?)\s*$")
BLOCKQUOTE_RE = re.compile(r"^(\s*>\s?)(.+?)\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*$")
REFERENCE_DEF_RE = re.compile(r"^\[[^\]]+\]:\s+\S+")
EXPLICIT_ANCHOR_RE = re.compile(r"^\([^)]+\)=$")
DIRECTIVE_OPTION_RE = re.compile(r"^\s*:[\w-]+:.*$")
DIRECTIVE_OPEN_RE = re.compile(r"^(```+|~~~+)\{([^}]+)\}(?:\s+(.*?))?\s*$")
FENCE_OPEN_RE = re.compile(r"^(```+|~~~+)")
HTML_TEXT_RE = re.compile(r"^(?P<prefix>\s*<[^>]+>)(?P<text>.*?)(?P<suffix></[^>]+>\s*)$")
PLACEHOLDER_RE = re.compile(r"%+\d+%+")


@dataclass(frozen=True)
class BatchDefinition:
    """Describe one translation batch.

    Attributes:
        label: User-facing batch label.
        include_prefixes: Directory prefixes to include.
        include_files: Individual Markdown files to include.
        exclude_files: Individual Markdown files to exclude.
    """

    label: str
    include_prefixes: tuple[str, ...] = ()
    include_files: tuple[str, ...] = ()
    exclude_files: tuple[str, ...] = ()


BATCHES = {
    1: BatchDefinition(
        label="Setup + onboarding overviews",
        include_prefixes=("Setup/",),
        include_files=(
            "Howtos/Howtos-Overview.md",
            "Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md",
        ),
    ),
    2: BatchDefinition(
        label="Remaining Howtos",
        include_prefixes=("Howtos/",),
        exclude_files=(
            "Howtos/Howtos-Overview.md",
            "Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md",
        ),
    ),
    3: BatchDefinition(label="Components", include_prefixes=("Components/",)),
    4: BatchDefinition(label="Concepts + Coding", include_prefixes=("Concepts/", "Coding/")),
    5: BatchDefinition(label="Contribs", include_prefixes=("Contribs/",)),
}


class TranslatorCache:
    """Tiny JSON cache for translated text segments."""

    def __init__(self, path: Path):
        """Initialize the cache.

        Args:
            path: Cache file path.
        """

        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))
        else:
            self.data = {}

    def get(self, key: str) -> str | None:
        """Get a cached translation.

        Args:
            key: Source text key.

        Returns:
            The translated string if present.
        """

        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        """Store a translation result.

        Args:
            key: Source text key.
            value: Translated text.
        """

        self.data[key] = value

    def flush(self) -> None:
        """Write cache contents to disk."""

        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )


class MarkdownZhTranslator:
    """Translate Markdown docs while preserving structure."""

    def __init__(self, cache: TranslatorCache, pause_seconds: float = 0.2):
        """Initialize the translator.

        Args:
            cache: Segment translation cache.
            pause_seconds: Pause between uncached translation requests.
        """

        self.cache = cache
        self.pause_seconds = pause_seconds
        self.google = GoogleTranslator(source="en", target="zh-TW")
        self.opencc = OpenCC("s2twp")

    def translate_file(self, path: Path) -> None:
        """Translate one Markdown file in place.

        Args:
            path: Markdown file path.
        """

        original_text = path.read_text(encoding="utf-8")
        translated_text = self._translate_markdown(original_text)
        path.write_text(translated_text, encoding="utf-8", newline="\n")

    def _translate_markdown(self, text: str) -> str:
        """Translate one Markdown document.

        Args:
            text: Markdown source.

        Returns:
            The translated Markdown.
        """

        lines = text.splitlines()
        translated = self._process_lines(lines)
        if text.endswith("\n"):
            return "\n".join(translated) + "\n"
        return "\n".join(translated)

    def _process_lines(self, lines: list[str]) -> list[str]:
        """Process Markdown lines recursively.

        Args:
            lines: Input lines.

        Returns:
            Processed lines.
        """

        output: list[str] = []
        heading_counts: dict[str, int] = {}
        index = 0
        while index < len(lines):
            line = lines[index]

            if not line.strip():
                output.append(line)
                index += 1
                continue

            if FENCE_OPEN_RE.match(line):
                fence_block, index = self._consume_fence_block(lines, index)
                output.extend(self._process_fence_block(fence_block))
                continue

            if REFERENCE_DEF_RE.match(line) or EXPLICIT_ANCHOR_RE.match(line):
                output.append(line)
                index += 1
                continue

            heading_match = HEADING_RE.match(line)
            if heading_match:
                hashes, heading = heading_match.groups()
                slug = self._make_unique_slug(self._slugify(heading), heading_counts)
                if slug and not self._previous_nonempty_is_anchor(output):
                    output.append(f"({slug})=")
                output.append(f"{hashes} {self._translate_text(heading, context='heading')}")
                index += 1
                continue

            if TABLE_SEPARATOR_RE.match(line):
                output.append(line)
                index += 1
                continue

            if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
                output.append(self._translate_table_row(line))
                index += 1
                continue

            if self._is_indented_code(line):
                code_block, index = self._consume_indented_block(lines, index)
                output.extend(code_block)
                continue

            bullet_match = BULLET_RE.match(line)
            if bullet_match:
                prefix, body = bullet_match.groups()
                output.append(f"{prefix}{self._translate_text(body)}")
                index += 1
                continue

            numbered_match = NUMBERED_RE.match(line)
            if numbered_match:
                prefix, body = numbered_match.groups()
                output.append(f"{prefix}{self._translate_text(body)}")
                index += 1
                continue

            blockquote_match = BLOCKQUOTE_RE.match(line)
            if blockquote_match:
                prefix, body = blockquote_match.groups()
                output.append(f"{prefix}{self._translate_text(body)}")
                index += 1
                continue

            html_match = HTML_TEXT_RE.match(line)
            if html_match and self._has_letters(html_match.group("text")):
                output.append(
                    f"{html_match.group('prefix')}"
                    f"{self._translate_text(html_match.group('text'))}"
                    f"{html_match.group('suffix')}"
                )
                index += 1
                continue

            paragraph_lines, index = self._consume_paragraph(lines, index)
            output.extend(self._translate_paragraph(paragraph_lines))

        return output

    def _consume_fence_block(self, lines: list[str], start: int) -> tuple[list[str], int]:
        """Consume a fenced code/directive block.

        Args:
            lines: Full document lines.
            start: Starting line index.

        Returns:
            The block lines and the index after the block.
        """

        open_line = lines[start]
        fence = FENCE_OPEN_RE.match(open_line).group(1)
        block = [open_line]
        index = start + 1
        while index < len(lines):
            block.append(lines[index])
            if lines[index].startswith(fence):
                return block, index + 1
            index += 1
        return block, index

    def _process_fence_block(self, block: list[str]) -> list[str]:
        """Translate a fenced block when safe.

        Args:
            block: Fenced block lines.

        Returns:
            Processed lines.
        """

        open_line = block[0]
        directive_match = DIRECTIVE_OPEN_RE.match(open_line)
        if not directive_match:
            return block

        fence, directive, title = directive_match.groups()
        directive_name = directive.strip().split()[0]
        if directive_name in PRESERVE_DIRECTIVES:
            return block
        if directive_name not in TRANSLATE_DIRECTIVES:
            return block

        rewritten = [open_line]
        if title:
            rewritten[0] = (
                f"{fence}{{{directive}}} {self._translate_text(title, context='heading')}"
            )

        inner = block[1:-1]
        prefix_lines: list[str] = []
        while inner and (not inner[0].strip() or DIRECTIVE_OPTION_RE.match(inner[0])):
            prefix_lines.append(inner.pop(0))
        rewritten.extend(prefix_lines)
        rewritten.extend(self._process_lines(inner))
        rewritten.append(block[-1])
        return rewritten

    def _consume_indented_block(self, lines: list[str], start: int) -> tuple[list[str], int]:
        """Consume an indented code block.

        Args:
            lines: Full document lines.
            start: Starting line index.

        Returns:
            The block lines and next index.
        """

        block: list[str] = []
        index = start
        while index < len(lines):
            line = lines[index]
            if line.startswith("    ") or line.startswith("\t") or not line.strip():
                block.append(line)
                index += 1
                continue
            break
        return block, index

    def _consume_paragraph(self, lines: list[str], start: int) -> tuple[list[str], int]:
        """Consume a paragraph-like line block.

        Args:
            lines: Full document lines.
            start: Starting line index.

        Returns:
            Paragraph lines and the next index.
        """

        block: list[str] = []
        index = start
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                break
            if (
                FENCE_OPEN_RE.match(line)
                or HEADING_RE.match(line)
                or REFERENCE_DEF_RE.match(line)
                or EXPLICIT_ANCHOR_RE.match(line)
                or TABLE_SEPARATOR_RE.match(line)
                or (line.lstrip().startswith("|") and line.rstrip().endswith("|"))
                or BULLET_RE.match(line)
                or NUMBERED_RE.match(line)
                or BLOCKQUOTE_RE.match(line)
                or self._is_indented_code(line)
            ):
                break
            block.append(line)
            index += 1
        return block, index

    def _translate_paragraph(self, lines: list[str]) -> list[str]:
        """Translate a paragraph block.

        Args:
            lines: Paragraph lines.

        Returns:
            Translated lines.
        """

        if not lines:
            return []
        joined = "\n".join(lines)
        translated = self._translate_text(joined)
        translated_lines = translated.splitlines()
        if len(translated_lines) == len(lines):
            return translated_lines
        return [self._translate_text(line) for line in lines]

    def _translate_table_row(self, line: str) -> str:
        """Translate one Markdown table row.

        Args:
            line: Table line.

        Returns:
            Translated table line.
        """

        leading = "|" if line.startswith("|") else ""
        trailing = "|" if line.endswith("|") else ""
        raw_cells = line.strip("|").split("|")
        translated_cells = []
        for cell in raw_cells:
            stripped = cell.strip()
            if not stripped:
                translated_cells.append(cell)
                continue
            translated = self._translate_text(stripped)
            left_pad = len(cell) - len(cell.lstrip(" "))
            right_pad = len(cell) - len(cell.rstrip(" "))
            translated_cells.append(f"{' ' * left_pad}{translated}{' ' * right_pad}")
        return leading + "|".join(translated_cells) + trailing

    def _translate_text(self, text: str, context: str = "body") -> str:
        """Translate one text fragment.

        Args:
            text: Input text.
            context: Translation context label.

        Returns:
            Translated text.
        """

        if not text or not self._has_letters(text):
            return text

        exact = EXACT_TRANSLATIONS.get(text.strip())
        if exact is not None:
            return exact

        cache_key = f"{context}:{text}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        protected_text, placeholders = self._protect_fragments(text)
        translated = self._translate_with_retry(protected_text)
        translated = self.opencc.convert(translated)
        restored = self._restore_fragments(translated, placeholders)
        restored = self._cleanup_translated_text(restored)
        self.cache.set(cache_key, restored)
        return restored

    def _translate_with_retry(self, text: str) -> str:
        """Translate text with a few retries.

        Args:
            text: Protected source text.

        Returns:
            Translated text.
        """

        last_error: Exception | None = None
        for attempt in range(3):
            try:
                result = self.google.translate(text)
                if result is None:
                    raise RuntimeError("translation returned no result")
                time.sleep(self.pause_seconds)
                return result
            except Exception as err:  # pragma: no cover - network dependent
                last_error = err
                time.sleep(self.pause_seconds * (attempt + 1))
        raise RuntimeError(f"Failed to translate text: {text[:120]!r}") from last_error

    def _protect_fragments(self, text: str) -> tuple[str, dict[str, str]]:
        """Protect Markdown and code-like fragments before translation.

        Args:
            text: Source text.

        Returns:
            Protected text and placeholder mapping.
        """

        placeholders: dict[str, str] = {}
        counter = 0

        def add_placeholder(fragment: str) -> str:
            nonlocal counter
            token = f"%%{counter}%%"
            placeholders[token] = fragment
            counter += 1
            return token

        def protect(pattern: str, value: str, flags: int = 0) -> str:
            compiled = re.compile(pattern, flags)
            return compiled.sub(
                lambda match: (
                    match.group(0)
                    if PLACEHOLDER_RE.fullmatch(match.group(0))
                    else add_placeholder(match.group(0))
                ),
                value,
            )

        protected = text
        protected = protect(r"`+[^`\n]+`+", protected)
        protected = re.sub(
            r"(?<=\]\()([^()]+)(?=\))",
            lambda match: (
                match.group(0)
                if PLACEHOLDER_RE.fullmatch(match.group(0))
                else add_placeholder(match.group(0))
            ),
            protected,
        )
        protected = re.sub(
            r"(?<=\]\[)([^\]]+)(?=\])",
            lambda match: (
                match.group(0)
                if PLACEHOLDER_RE.fullmatch(match.group(0))
                else add_placeholder(match.group(0))
            ),
            protected,
        )
        protected = protect(r"<https?://[^>]+>", protected)
        protected = protect(r"https?://[^\s)>\]]+", protected)
        protected = protect(r"</?[^>\n]+?>", protected)
        protected = protect(
            r"\b[A-Za-z0-9_./\\-]+\.(?:md|py|rst|html|css|txt|json|yml|yaml|ini|toml|po)\b",
            protected,
        )
        protected = protect(r"\b[a-z_]+(?:\.[a-z_][\w]*)+\b", protected)
        protected = protect(r"\b[a-z][\w]*_[\w_]+\b", protected)
        protected = protect(r"\b[A-Z][A-Za-z0-9]+(?:[A-Z][A-Za-z0-9]+)+\b", protected)
        protected = protect(r"\b[A-Z]{2,}[A-Z0-9_-]*\b", protected)
        protected = protect(r"@\w[\w-]*", protected)
        for term in sorted(GLOSSARY_TERMS, key=len, reverse=True):
            pattern = re.compile(rf"\b{re.escape(term)}\b", flags=re.IGNORECASE)
            protected = pattern.sub(lambda match: add_placeholder(match.group(0)), protected)
        return protected, placeholders

    def _restore_fragments(self, text: str, placeholders: dict[str, str]) -> str:
        """Restore protected fragments after translation.

        Args:
            text: Translated text with placeholders.
            placeholders: Placeholder mapping.

        Returns:
            Restored text.
        """

        restored = text
        for token, fragment in sorted(
            placeholders.items(), key=lambda item: len(item[0]), reverse=True
        ):
            marker = token.strip("%")
            restored = re.sub(
                rf"%+\s*{re.escape(marker)}\s*%+",
                lambda _match, replacement=fragment: replacement,
                restored,
            )
        return restored

    def _cleanup_translated_text(self, text: str) -> str:
        """Normalize a few translator artifacts.

        Args:
            text: Raw translated text.

        Returns:
            Cleaned text.
        """

        cleaned = text.replace("（ ", "（").replace(" ）", "）")
        cleaned = cleaned.replace("： ", "：")
        cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
        cleaned = re.sub(r"([（【「『])\s+", r"\1", cleaned)
        cleaned = re.sub(r"\s+([）】」』])", r"\1", cleaned)
        for original, replacement in POST_TRANSLATION_REPLACEMENTS.items():
            cleaned = cleaned.replace(original, replacement)
        return cleaned

    def _slugify(self, heading: str) -> str:
        """Generate an anchor slug from the original heading.

        Args:
            heading: Source heading text.

        Returns:
            Slugified heading.
        """

        stripped = re.sub(r"`([^`]*)`", r"\1", heading)
        stripped = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)
        normalized = (
            unicodedata.normalize("NFKD", stripped).encode("ascii", "ignore").decode("ascii")
        )
        normalized = normalized.lower()
        normalized = re.sub(r"[^\w\s-]", "", normalized)
        normalized = re.sub(r"[-\s]+", "-", normalized).strip("-")
        return normalized

    def _make_unique_slug(self, slug: str, counts: dict[str, int]) -> str:
        """Ensure heading anchors stay unique within a file.

        Args:
            slug: Base slug.
            counts: Existing slug counts.

        Returns:
            Unique slug.
        """

        if not slug:
            return slug
        if slug not in counts:
            counts[slug] = 0
            return slug
        counts[slug] += 1
        return f"{slug}-{counts[slug]}"

    @staticmethod
    def _previous_nonempty_is_anchor(lines: list[str]) -> bool:
        """Check whether the previous non-empty line is an explicit anchor.

        Args:
            lines: Output lines accumulated so far.

        Returns:
            ``True`` if the previous non-empty line is an anchor.
        """

        for line in reversed(lines):
            if not line.strip():
                continue
            return bool(EXPLICIT_ANCHOR_RE.match(line))
        return False

    @staticmethod
    def _has_letters(text: str) -> bool:
        """Return whether the text contains Latin letters.

        Args:
            text: Input text.

        Returns:
            ``True`` if the text contains Latin letters.
        """

        return bool(re.search(r"[A-Za-z]", text))

    @staticmethod
    def _is_indented_code(line: str) -> bool:
        """Best-effort detection for indented code blocks.

        Args:
            line: Input line.

        Returns:
            ``True`` if the line looks like indented code.
        """

        stripped = line.lstrip(" ")
        return (
            line.startswith("    ")
            and not BULLET_RE.match(stripped)
            and not NUMBERED_RE.match(stripped)
        )


def contains_cjk(text: str) -> bool:
    """Check whether a text contains CJK characters.

    Args:
        text: Input text.

    Returns:
        ``True`` if the text contains CJK characters.
    """

    return bool(re.search(r"[\u3400-\u9fff]", text))


def discover_markdown_files() -> list[Path]:
    """Return all reader-facing Markdown files under ``docs/source``.

    Returns:
        Sorted Markdown file paths.
    """

    return sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if API_ROOT not in path.parents and path != API_ROOT
    )


def is_english_source(path: Path) -> bool:
    """Determine whether a Markdown file still needs translation.

    Args:
        path: Markdown path.

    Returns:
        ``True`` if the file appears to still be English-only.
    """

    return not contains_cjk(path.read_text(encoding="utf-8"))


def select_batch_files(batch_number: int) -> list[Path]:
    """Select Markdown files for one batch.

    Args:
        batch_number: Batch number from ``BATCHES``.

    Returns:
        Paths included in the batch.
    """

    definition = BATCHES[batch_number]
    selected: list[Path] = []
    for path in discover_markdown_files():
        relative = path.relative_to(SOURCE_ROOT).as_posix()
        if not is_english_source(path):
            continue
        if relative in definition.exclude_files:
            continue
        if relative in definition.include_files:
            selected.append(path)
            continue
        if any(relative.startswith(prefix) for prefix in definition.include_prefixes):
            selected.append(path)
    return sorted(selected)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed arguments.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--batch",
        type=int,
        action="append",
        choices=sorted(BATCHES),
        help="Translate one or more predefined batches.",
    )
    parser.add_argument(
        "--path",
        action="append",
        help="Translate one or more specific Markdown paths relative to docs/source.",
    )
    parser.add_argument(
        "--pause-seconds",
        type=float,
        default=0.2,
        help="Pause between uncached translation requests.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the files that would be translated without changing them.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the batch translation helper."""

    args = parse_args()
    paths: set[Path] = set()

    if args.batch:
        for batch_number in args.batch:
            paths.update(select_batch_files(batch_number))

    if args.path:
        for relative in args.path:
            path = (SOURCE_ROOT / relative).resolve()
            if not path.exists():
                raise SystemExit(f"Path does not exist: {relative}")
            paths.add(path)

    if not paths:
        raise SystemExit("No files selected. Use --batch and/or --path.")

    selected = sorted(paths)
    if args.dry_run:
        for path in selected:
            print(path.relative_to(SOURCE_ROOT).as_posix())
        return

    cache = TranslatorCache(CACHE_PATH)
    translator = MarkdownZhTranslator(cache=cache, pause_seconds=args.pause_seconds)

    for index, path in enumerate(selected, start=1):
        relative = path.relative_to(SOURCE_ROOT).as_posix()
        print(f"[{index}/{len(selected)}] Translating {relative}")
        translator.translate_file(path)
        cache.flush()


if __name__ == "__main__":
    main()
