#!/usr/bin/env python3
"""Organize files in one directory into category folders.

The script runs in dry-run mode by default. Use --apply to perform moves.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".json", ".yml", ".yaml"},
}


def category_for(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def unique_destination(destination: Path) -> Path:
    """Return a non-conflicting destination path."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def organize_directory(directory: Path, apply_changes: bool = False) -> list[str]:
    """Plan or apply file moves for files directly inside directory."""
    actions: list[str] = []

    for item in sorted(directory.iterdir()):
        if not item.is_file():
            continue

        category = category_for(item)
        destination_dir = directory / category
        destination = unique_destination(destination_dir / item.name)

        actions.append(f"{item.name} -> {category}/{destination.name}")

        if apply_changes:
            destination_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))

    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by file type."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this flag, only a dry run is shown.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.directory.exists() or not args.directory.is_dir():
        raise SystemExit(f"Directory not found: {args.directory}")

    actions = organize_directory(args.directory, apply_changes=args.apply)

    print("FILE ORGANIZER")
    print("=" * 14)
    print(f"Directory: {args.directory.resolve()}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY RUN'}\n")

    if not actions:
        print("No files found to organize.")
        return

    for action in actions:
        print(action)

    if not args.apply:
        print("\nNo files were moved. Re-run with --apply to perform these actions.")


if __name__ == "__main__":
    main()
