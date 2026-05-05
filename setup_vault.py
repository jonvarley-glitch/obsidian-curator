#!/usr/bin/env python3
"""Vault Forge: Scaffold an Obsidian vault for a Solution Architect.

Reads config.yaml and creates the full vault structure including folders,
templates, starter content, .obsidian configs, and community plugins.

Safe to re-run -- never overwrites existing user notes.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
GITHUB_API = "https://api.github.com/repos"
REQUEST_TIMEOUT = 30


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

@dataclass
class PluginSpec:
    id: str
    repo: str


@dataclass
class VaultConfig:
    name: str
    path: Path
    folders: list[str]
    plugins: list[PluginSpec]
    core_plugins: dict[str, bool]
    app_settings: dict[str, Any]
    community_plugin_ids: list[str]
    note_types: list[str] = field(default_factory=list)
    gitignore_lines: list[str] = field(default_factory=list)


class ConfigError(ValueError):
    """Raised when config.yaml is missing required keys or has invalid values."""


def load_config(config_path: Path) -> VaultConfig:
    """Load and validate config.yaml into a typed VaultConfig.

    Raises ConfigError if the file is structurally invalid.
    """
    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if "vault" not in raw or not isinstance(raw["vault"], dict):
        raise ConfigError("config.yaml: missing required 'vault' section")
    vault_section = raw["vault"]
    for required in ("name", "path"):
        if not vault_section.get(required):
            raise ConfigError(f"config.yaml: vault.{required} is required")

    vault_path = Path(vault_section["path"]).expanduser().resolve()

    plugins: list[PluginSpec] = []
    for i, p in enumerate(raw.get("plugins") or []):
        if not isinstance(p, dict) or "id" not in p or "repo" not in p:
            raise ConfigError(
                f"config.yaml: plugins[{i}] must have 'id' and 'repo' fields",
            )
        if "/" not in p["repo"]:
            raise ConfigError(
                f"config.yaml: plugins[{i}].repo must be 'owner/name', got "
                f"'{p['repo']}'",
            )
        plugins.append(PluginSpec(id=p["id"], repo=p["repo"]))

    core_map: dict[str, bool] = {}
    for pid in raw.get("core_plugins", {}).get("enable", []):
        core_map[pid] = True
    for pid in raw.get("core_plugins", {}).get("disable", []):
        core_map[pid] = False

    gitignore = [
        ".obsidian/workspace.json",
        ".obsidian/workspace-mobile.json",
        ".obsidian/graph.json",
        ".obsidian/backlink.json",
        ".obsidian/.obsidian-git-data",
        "conflict-files-obsidian-git.md",
        ".smart-connections/",
        ".trash/",
        ".DS_Store",
        "Thumbs.db",
    ]

    return VaultConfig(
        name=vault_section["name"],
        path=vault_path,
        folders=raw.get("folders") or [],
        plugins=plugins,
        core_plugins=core_map,
        app_settings=raw.get("app_settings") or {},
        community_plugin_ids=[p.id for p in plugins],
        note_types=raw.get("note_types") or [],
        gitignore_lines=gitignore,
    )


_TEMPLATE_TYPE_RE = re.compile(r"^type:\s*(\S+)\s*$", re.MULTILINE)


def scan_template_types(templates_dir: Path) -> dict[str, str | None]:
    """Return {filename: type} parsed from template frontmatter.

    Skips Templater dynamic placeholders (`<% ... %>`) -- only literal
    `type: <value>` lines are returned. Files without such a line map to None.
    """
    types: dict[str, str | None] = {}
    for f in sorted(templates_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        match = _TEMPLATE_TYPE_RE.search(text)
        if match and not match.group(1).startswith("<%"):
            types[f.name] = match.group(1)
        else:
            types[f.name] = None
    return types


def validate_config(
    config: VaultConfig,
    templates_dir: Path | None = None,
) -> list[str]:
    """Run lightweight semantic checks beyond structural parsing.

    Returns a list of human-readable warnings/errors (empty if all clean).
    Does not raise -- caller decides how to react.

    When `templates_dir` is provided (or defaults to PROJECT_ROOT/templates),
    every `*.md` template's `type:` frontmatter is checked against
    `config.note_types` so typos and forgotten config updates are caught.
    """
    issues: list[str] = []
    if not config.folders:
        issues.append("folders: list is empty")
    if not config.plugins:
        issues.append("plugins: no community plugins configured")
    if not config.app_settings:
        issues.append("app_settings: empty (vault will use Obsidian defaults)")
    seen_ids: set[str] = set()
    for plugin in config.plugins:
        if plugin.id in seen_ids:
            issues.append(f"plugins: duplicate id '{plugin.id}'")
        seen_ids.add(plugin.id)

    if templates_dir is None:
        templates_dir = PROJECT_ROOT / "templates"
    if config.note_types and templates_dir.is_dir():
        allowed = set(config.note_types)
        for filename, t in scan_template_types(templates_dir).items():
            if t is None:
                issues.append(
                    f"templates/{filename}: missing literal 'type:' in frontmatter",
                )
            elif t not in allowed:
                issues.append(
                    f"templates/{filename}: type '{t}' not in note_types",
                )
    return issues


def print_summary(config: VaultConfig) -> None:
    """Print a human-readable summary of the loaded config."""
    logger.info("Vault name:       %s", config.name)
    logger.info("Vault path:       %s", config.path)
    logger.info("Folders:          %d", len(config.folders))
    logger.info("Community plugins: %d", len(config.plugins))
    enabled = sum(1 for v in config.core_plugins.values() if v)
    disabled = sum(1 for v in config.core_plugins.values() if not v)
    logger.info("Core plugins:     %d enabled, %d disabled", enabled, disabled)
    logger.info("App settings:     %d keys", len(config.app_settings))
    logger.info("Note types:       %d", len(config.note_types))


# ---------------------------------------------------------------------------
# Folder creation
# ---------------------------------------------------------------------------

def create_folders(config: VaultConfig) -> None:
    """Create the vault folder tree."""
    for folder_name in config.folders:
        folder_path = config.path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        logger.info("Folder: %s", folder_name)


# ---------------------------------------------------------------------------
# Template and content copying
# ---------------------------------------------------------------------------

def copy_templates(config: VaultConfig) -> None:
    """Copy template files into the vault's Templates/ folder."""
    src_dir = PROJECT_ROOT / "templates"
    dest_dir = config.path / "Templates"
    dest_dir.mkdir(parents=True, exist_ok=True)

    for src_file in sorted(src_dir.glob("*.md")):
        dest_file = dest_dir / src_file.name
        shutil.copy2(src_file, dest_file)
        logger.info("Template: Templates/%s", src_file.name)


def copy_prompts(config: VaultConfig) -> None:
    """Copy prompt templates into the vault's Prompts/ folder."""
    src_dir = PROJECT_ROOT / "prompts"
    dest_dir = config.path / "Prompts"
    dest_dir.mkdir(parents=True, exist_ok=True)

    for src_file in sorted(src_dir.glob("*.md")):
        dest_file = dest_dir / src_file.name
        shutil.copy2(src_file, dest_file)
        logger.info("Prompt: Prompts/%s", src_file.name)


_STARTER_CONTENT_NAMES = {
    "Home.md",
    "CLAUDE.md",
    "Conventions.md",
    "Getting Started.md",
}


def copy_starter_content(config: VaultConfig) -> None:
    """Copy starter content (Home, CLAUDE, Conventions, Getting Started) to vault root.

    Never overwrites existing files to protect user edits. Other markdown files
    in `content/` (e.g. Task Board.md) are placed by their own dedicated copy
    step into the right folder.
    """
    src_dir = PROJECT_ROOT / "content"
    for src_file in sorted(src_dir.glob("*.md")):
        if src_file.name not in _STARTER_CONTENT_NAMES:
            continue
        dest_file = config.path / src_file.name
        if dest_file.exists():
            logger.warning("Skipped (exists): %s", src_file.name)
            continue
        shutil.copy2(src_file, dest_file)
        logger.info("Content: %s", src_file.name)


def copy_bases(config: VaultConfig) -> None:
    """Copy starter `.base` files into the vault's Bases/ folder.

    Idempotent: never overwrites a `.base` the user has customised.
    """
    src_dir = PROJECT_ROOT / "content" / "bases"
    if not src_dir.exists():
        return
    dest_dir = config.path / "Bases"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(src_dir.glob("*.base")):
        dest_file = dest_dir / src_file.name
        if dest_file.exists():
            logger.warning("Skipped (exists): Bases/%s", src_file.name)
            continue
        shutil.copy2(src_file, dest_file)
        logger.info("Base: Bases/%s", src_file.name)


def copy_kanban(config: VaultConfig) -> None:
    """Copy the starter Task Board into 13-Tasks/ if not already present.

    Idempotent: never overwrites an existing board.
    """
    src_file = PROJECT_ROOT / "content" / "Task Board.md"
    if not src_file.exists():
        return
    dest_dir = config.path / "13-Tasks"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "Task Board.md"
    if dest_file.exists():
        logger.warning("Skipped (exists): 13-Tasks/Task Board.md")
        return
    shutil.copy2(src_file, dest_file)
    logger.info("Kanban: 13-Tasks/Task Board.md")


# ---------------------------------------------------------------------------
# Obsidian config
# ---------------------------------------------------------------------------

def write_obsidian_config(config: VaultConfig) -> None:
    """Write .obsidian/ JSON configuration files (top-level and per-plugin).

    `app.json` is special: the shipped file acts as a structural shell, then
    `config.app_settings` is merged on top (config wins). It is rewritten on
    every run so config edits propagate. All other top-level JSONs are
    idempotent -- if the destination exists, it is left alone so user changes
    made via Obsidian's settings UI are preserved.
    """
    obsidian_dir = config.path / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    src_dir = PROJECT_ROOT / "obsidian_config"
    for src_file in sorted(src_dir.glob("*.json")):
        dest_file = obsidian_dir / src_file.name
        if src_file.name == "app.json":
            base = json.loads(src_file.read_text(encoding="utf-8"))
            merged = {**base, **config.app_settings}
            dest_file.write_text(
                json.dumps(merged, indent=2) + "\n", encoding="utf-8",
            )
            logger.info("Config: .obsidian/app.json (merged from config.yaml)")
            continue
        if dest_file.exists():
            logger.warning("Skipped (exists): .obsidian/%s", src_file.name)
            continue
        shutil.copy2(src_file, dest_file)
        logger.info("Config: .obsidian/%s", src_file.name)


def write_plugin_configs(config: VaultConfig) -> None:
    """Copy per-plugin data.json files into .obsidian/plugins/<id>/data.json.

    Runs after install_plugins so the destination directories exist. Existing
    plugin data files are not overwritten -- protects user customisations.
    """
    src_root = PROJECT_ROOT / "obsidian_config" / "plugins"
    if not src_root.exists():
        return
    dest_root = config.path / ".obsidian" / "plugins"
    for src_file in sorted(src_root.glob("*/data.json")):
        plugin_id = src_file.parent.name
        dest_dir = dest_root / plugin_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "data.json"
        if dest_file.exists():
            logger.warning(
                "Skipped (exists): .obsidian/plugins/%s/data.json", plugin_id,
            )
            continue
        shutil.copy2(src_file, dest_file)
        logger.info("Plugin config: .obsidian/plugins/%s/data.json", plugin_id)


# ---------------------------------------------------------------------------
# Plugin installation
# ---------------------------------------------------------------------------

def download_plugin(plugin: PluginSpec, plugins_dir: Path) -> bool:
    """Download a plugin's latest release from GitHub and install it.

    Returns True on success, False on failure.
    """
    plugin_dir = plugins_dir / plugin.id
    manifest_path = plugin_dir / "manifest.json"

    if manifest_path.exists():
        logger.info("Plugin (cached): %s", plugin.id)
        return True

    url = f"{GITHUB_API}/{plugin.repo}/releases/latest"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Failed to fetch release for %s: %s", plugin.id, exc)
        return False

    release = resp.json()
    assets = {a["name"]: a["browser_download_url"] for a in release.get("assets", [])}

    required_files = ["main.js", "manifest.json"]
    optional_files = ["styles.css"]

    if not all(f in assets for f in required_files):
        logger.error(
            "Plugin %s release missing required files (have: %s)",
            plugin.id,
            list(assets.keys()),
        )
        return False

    plugin_dir.mkdir(parents=True, exist_ok=True)

    for filename in required_files + optional_files:
        if filename not in assets:
            continue
        try:
            file_resp = requests.get(assets[filename], timeout=REQUEST_TIMEOUT)
            file_resp.raise_for_status()
            (plugin_dir / filename).write_bytes(file_resp.content)
        except requests.RequestException as exc:
            logger.error("Failed to download %s/%s: %s", plugin.id, filename, exc)
            if filename in required_files:
                shutil.rmtree(plugin_dir, ignore_errors=True)
                return False

    logger.info("Plugin (installed): %s", plugin.id)
    return True


def install_plugins(config: VaultConfig) -> None:
    """Download and install all community plugins."""
    plugins_dir = config.path / ".obsidian" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0
    for plugin in config.plugins:
        if download_plugin(plugin, plugins_dir):
            success += 1
        else:
            failed += 1

    logger.info(
        "Plugins: %d installed, %d failed (out of %d)",
        success,
        failed,
        len(config.plugins),
    )


# ---------------------------------------------------------------------------
# Vault .gitignore
# ---------------------------------------------------------------------------

def write_vault_gitignore(config: VaultConfig) -> None:
    """Write the vault's `.gitignore` from `config.gitignore_lines`.

    Always rewrites the file so updates to the ignore list propagate. Does
    not run `git init` -- the user opts into version control themselves.
    """
    gitignore_path = config.path / ".gitignore"
    content = "\n".join(config.gitignore_lines) + "\n"
    gitignore_path.write_text(content, encoding="utf-8")
    logger.info("Created .gitignore")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def setup_vault(
    config_path: Path | None = None,
    vault_path_override: Path | None = None,
    skip_plugins: bool = False,
) -> None:
    """Run the full vault setup pipeline.

    Args:
        config_path: Path to config.yaml. Defaults to project root.
        vault_path_override: Optional override for the vault.path from config.
        skip_plugins: If True, do not download community plugins (offline / CI).
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    config = load_config(config_path)

    if vault_path_override is not None:
        config.path = vault_path_override.expanduser().resolve()

    logger.info("=" * 60)
    logger.info("Vault Forge -- Setting up: %s", config.name)
    logger.info("Target: %s", config.path)
    logger.info("=" * 60)

    config.path.mkdir(parents=True, exist_ok=True)

    create_folders(config)
    copy_templates(config)
    copy_prompts(config)
    copy_starter_content(config)
    copy_bases(config)
    copy_kanban(config)
    write_obsidian_config(config)
    if skip_plugins:
        logger.info("Skipping plugin downloads (--skip-plugins)")
    else:
        install_plugins(config)
    write_plugin_configs(config)
    write_vault_gitignore(config)

    logger.info("=" * 60)
    logger.info("Vault setup complete!")
    logger.info("Open Obsidian -> Open folder as vault -> %s", config.path)
    logger.info("=" * 60)


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Kept private to setup_vault; callers should invoke `main()` instead.
    """
    parser = argparse.ArgumentParser(
        prog="setup_vault.py",
        description="Scaffold an Obsidian vault for a Solution Architect.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config.yaml (default: ./config.yaml).",
    )
    parser.add_argument(
        "--vault-path",
        type=Path,
        default=None,
        help="Override vault.path from config (useful for tests / dry runs).",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Parse and validate config, print summary, do not write any files.",
    )
    parser.add_argument(
        "--skip-plugins",
        action="store_true",
        help="Skip plugin downloads (offline use, CI).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Returns a Unix-style exit code: 0 on success, 1 on config / validation
    errors. With `--validate`, no files are written.
    """
    args = _build_arg_parser().parse_args(argv)
    config_path = args.config or PROJECT_ROOT / "config.yaml"

    if args.validate:
        if not config_path.exists():
            logger.error("Config not found: %s", config_path)
            return 1
        try:
            config = load_config(config_path)
        except ConfigError as exc:
            logger.error("Config error: %s", exc)
            return 1
        if args.vault_path is not None:
            config.path = args.vault_path.expanduser().resolve()
        print_summary(config)
        issues = validate_config(config)
        if issues:
            for issue in issues:
                logger.warning("Validation: %s", issue)
        else:
            logger.info("Validation: OK")
        return 0

    setup_vault(
        config_path=config_path,
        vault_path_override=args.vault_path,
        skip_plugins=args.skip_plugins,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
