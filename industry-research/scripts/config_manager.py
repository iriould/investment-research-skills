#!/usr/bin/env python3
"""Read and update investment-research standalone skill runtime config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CONFIG_NAME = "investment-research-config.json"
DEFAULT_CONFIG: dict[str, str] = {
    "primary_search_tools": "auto",
    "technical_search_tools": "auto",
    "search_language_bias": "zh-first",
    "collaboration_mode": "ask",
    "lark_reference_mode": "ask",
}
ALLOWED_KEYS = set(DEFAULT_CONFIG)


def config_path() -> Path:
    skill_dir = Path(__file__).resolve().parent.parent
    return skill_dir / "config" / CONFIG_NAME


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        return dict(DEFAULT_CONFIG)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
    config = dict(DEFAULT_CONFIG)
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ALLOWED_KEYS and isinstance(value, str):
                config[key] = value
    return config


def save_config(config: dict[str, Any]) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    filtered = {
        key: str(config.get(key, DEFAULT_CONFIG[key]))
        for key in DEFAULT_CONFIG
    }
    path.write_text(
        json.dumps(filtered, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("path")
    subparsers.add_parser("get")
    init_parser = subparsers.add_parser("init")
    set_parser = subparsers.add_parser("set")

    for target in (init_parser, set_parser):
        target.add_argument("--primary-search-tools")
        target.add_argument("--technical-search-tools")
        target.add_argument("--search-language-bias")
        target.add_argument("--collaboration-mode")
        target.add_argument("--lark-reference-mode")

    args = parser.parse_args()

    if args.command == "path":
        print(config_path())
        return 0

    if args.command == "get":
        print(json.dumps(load_config(), ensure_ascii=False, indent=2))
        return 0

    config = load_config() if args.command == "set" else dict(DEFAULT_CONFIG)
    updates = {
        "primary_search_tools": args.primary_search_tools,
        "technical_search_tools": args.technical_search_tools,
        "search_language_bias": args.search_language_bias,
        "collaboration_mode": args.collaboration_mode,
        "lark_reference_mode": args.lark_reference_mode,
    }
    for key, value in updates.items():
        if value is not None:
            config[key] = value
    path = save_config(config)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




