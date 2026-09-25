#!/usr/bin/env python3
"""Validate structural consistency between Japanese and English Docusaurus docs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

DOC_SUFFIXES = {".md", ".mdx"}
JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
PRESERVE_FRONT_MATTER_VALUES = {
    "id",
    "slug",
    "sidebar_position",
    "pagination_next",
    "pagination_prev",
    "custom_edit_url",
}
DISPLAY_FRONT_MATTER_KEYS = {"title", "description", "sidebar_label"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that an English Docusaurus translation preserves source document structure."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--source-dir", default="docs")
    parser.add_argument(
        "--target-dir",
        default="i18n/en/docusaurus-plugin-content-docs/current",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=None,
        help="Optional source-relative .md/.mdx paths to validate.",
    )
    parser.add_argument(
        "--json-files",
        nargs="*",
        default=None,
        help=(
            "Optional Docusaurus docs translation JSON filenames relative to "
            "i18n/en/docusaurus-plugin-content-docs. If omitted, current.json "
            "is checked when present."
        ),
    )
    return parser.parse_args()


def normalize_relative_file(value: str, source_dir: Path) -> Path:
    path = Path(value.replace("\\", "/"))
    try:
        return path.relative_to(source_dir)
    except ValueError:
        return path


def collect_source_files(source_root: Path, files: list[str] | None) -> list[Path]:
    if files:
        rels = [normalize_relative_file(value, Path(source_root.name)) for value in files]
        return [source_root / rel for rel in rels]
    return sorted(path for path in source_root.rglob("*") if path.suffix.lower() in DOC_SUFFIXES)


def split_front_matter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    return "", text


def extract_top_level_front_matter(front_matter: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
    for line in front_matter.splitlines():
        if line.startswith((" ", "\t")):
            continue
        match = pattern.match(line)
        if match:
            values[match.group(1)] = (match.group(2) or "").strip()
    return values


def extract_fenced_blocks(text: str) -> list[str]:
    lines = text.splitlines()
    blocks: list[str] = []
    current: list[str] | None = None
    fence_char = ""
    fence_len = 0

    opener = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
    for line in lines:
        if current is None:
            match = opener.match(line)
            if not match:
                continue
            fence = match.group(1)
            current = [line]
            fence_char = fence[0]
            fence_len = len(fence)
            continue

        current.append(line)
        stripped = line.lstrip()
        if stripped.startswith(fence_char * fence_len):
            closing = stripped.split()[0] if stripped.split() else stripped
            if closing and set(closing) == {fence_char} and len(closing) >= fence_len:
                blocks.append("\n".join(current))
                current = None
                fence_char = ""
                fence_len = 0

    if current is not None:
        blocks.append("\n".join(current))
    return blocks


def remove_fenced_blocks(text: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    opener = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")

    for line in lines:
        if not in_fence:
            match = opener.match(line)
            if match:
                fence = match.group(1)
                in_fence = True
                fence_char = fence[0]
                fence_len = len(fence)
                result.append("")
            else:
                result.append(line)
            continue

        stripped = line.lstrip()
        if stripped.startswith(fence_char * fence_len):
            closing = stripped.split()[0] if stripped.split() else stripped
            if closing and set(closing) == {fence_char} and len(closing) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
        result.append("")
    return "\n".join(result)


def extract_inline_code(text: str) -> list[str]:
    text = remove_fenced_blocks(text)
    pattern = re.compile(r"(?<!`)(`{1,2})([^`\n]+?)\1(?!`)")
    return [match.group(0) for match in pattern.finditer(text)]


def extract_link_targets(text: str) -> list[str]:
    text = remove_fenced_blocks(text)
    inline_pattern = re.compile(r"!?\[[^\]]*\]\(\s*([^\s)]+)")
    reference_pattern = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
    values = [match.group(1) for match in inline_pattern.finditer(text)]
    values.extend(match.group(1) for match in reference_pattern.finditer(text))
    return values


def compare_counter(label: str, source_values: list[str], target_values: list[str], errors: list[str]) -> None:
    if Counter(source_values) != Counter(target_values):
        errors.append(f"{label} が原文と一致しません")


def validate_pair(source_path: Path, target_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    source_text = source_path.read_text(encoding="utf-8")
    target_text = target_path.read_text(encoding="utf-8")
    source_front, source_body = split_front_matter(source_text)
    target_front, target_body = split_front_matter(target_text)
    source_meta = extract_top_level_front_matter(source_front)
    target_meta = extract_top_level_front_matter(target_front)

    for key in source_meta:
        if key not in target_meta:
            errors.append(f"front matterキー '{key}' が英語版にありません")
    for key in target_meta:
        if key not in source_meta:
            warnings.append(f"英語版だけにfront matterキー '{key}' があります")

    for key in PRESERVE_FRONT_MATTER_VALUES:
        if key in source_meta and source_meta[key] != target_meta.get(key):
            errors.append(
                f"front matter '{key}' の値が変更されています: "
                f"{source_meta[key]!r} != {target_meta.get(key)!r}"
            )

    for key in DISPLAY_FRONT_MATTER_KEYS:
        if key in source_meta and key in target_meta and source_meta[key] == target_meta[key]:
            if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", source_meta[key]):
                warnings.append(f"front matter '{key}' が日本語のままです")

    compare_counter("fenced code block", extract_fenced_blocks(source_body), extract_fenced_blocks(target_body), errors)
    compare_counter("インラインコード", extract_inline_code(source_body), extract_inline_code(target_body), errors)
    compare_counter("リンク先または画像パス", extract_link_targets(source_body), extract_link_targets(target_body), errors)

    return errors, warnings



def validate_translation_json(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"JSONを読み込めません: {exc}"], warnings

    if not isinstance(data, dict):
        return ["JSONのトップレベルがobjectではありません"], warnings

    for key, entry in data.items():
        if not isinstance(entry, dict):
            errors.append(f"{key!r}: エントリがobjectではありません")
            continue
        if "message" not in entry:
            errors.append(f"{key!r}: 'message' がありません")
            continue
        message = entry["message"]
        if not isinstance(message, str):
            errors.append(f"{key!r}: 'message' が文字列ではありません")
            continue
        if JAPANESE_RE.search(message):
            warnings.append(f"{key!r}: 'message' に日本語が残っています: {message!r}")

    return errors, warnings


def collect_json_files(plugin_i18n_root: Path, requested: list[str] | None) -> list[Path]:
    if requested is not None:
        return [plugin_i18n_root / value for value in requested]
    current = plugin_i18n_root / "current.json"
    return [current] if current.is_file() else []

def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    source_root = (repo_root / args.source_dir).resolve()
    target_root = (repo_root / args.target_dir).resolve()

    if not source_root.is_dir():
        print(f"ERROR: 原文ディレクトリがありません: {source_root}")
        return 2
    if not target_root.is_dir():
        print(f"ERROR: 英語版ディレクトリがありません: {target_root}")
        return 2

    source_files = collect_source_files(source_root, args.files)
    errors_total = 0
    warnings_total = 0
    checked = 0

    for source_path in source_files:
        if source_path.suffix.lower() not in DOC_SUFFIXES:
            continue
        try:
            relative = source_path.relative_to(source_root)
        except ValueError:
            print(f"ERROR: 原文ディレクトリ外のファイルです: {source_path}")
            errors_total += 1
            continue

        if not source_path.is_file():
            print(f"ERROR: 原文ファイルがありません: {relative}")
            errors_total += 1
            continue

        target_path = target_root / relative
        if not target_path.is_file():
            print(f"ERROR: {relative}: 英語版ファイルがありません")
            errors_total += 1
            continue

        checked += 1
        errors, warnings = validate_pair(source_path, target_path)
        for message in errors:
            print(f"ERROR: {relative}: {message}")
        for message in warnings:
            print(f"WARNING: {relative}: {message}")
        errors_total += len(errors)
        warnings_total += len(warnings)

    if args.files is None:
        source_rel = {
            path.relative_to(source_root)
            for path in source_root.rglob("*")
            if path.suffix.lower() in DOC_SUFFIXES
        }
        for target_path in sorted(
            path for path in target_root.rglob("*") if path.suffix.lower() in DOC_SUFFIXES
        ):
            relative = target_path.relative_to(target_root)
            if relative not in source_rel:
                print(f"WARNING: {relative}: 日本語原文に対応するファイルがありません")
                warnings_total += 1

    plugin_i18n_root = target_root.parent
    json_checked = 0
    for json_path in collect_json_files(plugin_i18n_root, args.json_files):
        if not json_path.is_file():
            print(f"ERROR: JSON翻訳ファイルがありません: {json_path}")
            errors_total += 1
            continue
        json_checked += 1
        errors, warnings = validate_translation_json(json_path)
        relative = json_path.relative_to(plugin_i18n_root)
        for message in errors:
            print(f"ERROR: {relative}: {message}")
        for message in warnings:
            print(f"WARNING: {relative}: {message}")
        errors_total += len(errors)
        warnings_total += len(warnings)

    print(
        f"Checked {checked} document file(s) and {json_checked} JSON file(s): "
        f"{errors_total} error(s), {warnings_total} warning(s)."
    )
    return 1 if errors_total else 0


if __name__ == "__main__":
    sys.exit(main())
