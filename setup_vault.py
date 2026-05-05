#!/usr/bin/env python3
"""Vault Forge: Scaffold an Obsidian vault for an Elastic Solution Architect.

Reads config.yaml and creates the full vault structure including folders,
templates, starter content, .obsidian configs, and community plugins.

Safe to re-run -- never overwrites existing user notes.
"""
from __future__ import annotations

import io
import json
import logging
import shutil
import zipfile
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
    gitignore_lines: list[str] = field(default_factory=list)


def load_config(config_path: Path) -> VaultConfig:
    """Load and validate config.yaml into a typed VaultConfig."""
    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    vault_path = Path(raw["vault"]["path"]).expanduser().resolve()

    plugins = [
        PluginSpec(id=p["id"], repo=p["repo"])
        for p in raw.get("plugins", [])
    ]

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
        name=raw["vault"]["name"],
        path=vault_path,
        folders=raw.get("folders", []),
        plugins=plugins,
        core_plugins=core_map,
        app_settings=raw.get("app_settings", {}),
        community_plugin_ids=[p["id"] for p in raw.get("plugins", [])],
        gitignore_lines=gitignore,
    )


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


def copy_starter_content(config: VaultConfig) -> None:
    """Copy starter content to vault root.

    Includes Home.md, CLAUDE.md, Conventions.md, Getting Started.md.
    Never overwrites existing files to protect user edits.
    """
    src_dir = PROJECT_ROOT / "content"
    for src_file in sorted(src_dir.glob("*.md")):
        dest_file = config.path / src_file.name
        if dest_file.exists():
            logger.warning("Skipped (exists): %s", src_file.name)
            continue
        shutil.copy2(src_file, dest_file)
        logger.info("Content: %s", src_file.name)


# ---------------------------------------------------------------------------
# Obsidian config
# ---------------------------------------------------------------------------

def write_obsidian_config(config: VaultConfig) -> None:
    """Write .obsidian/ JSON configuration files."""
    obsidian_dir = config.path / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    src_dir = PROJECT_ROOT / "obsidian_config"
    for src_file in sorted(src_dir.glob("*.json")):
        dest_file = obsidian_dir / src_file.name
        shutil.copy2(src_file, dest_file)
        logger.info("Config: .obsidian/%s", src_file.name)


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
# Git initialisation
# ---------------------------------------------------------------------------

def init_git(config: VaultConfig) -> None:
    """Create .gitignore in the vault. Does not run git init."""
    gitignore_path = config.path / ".gitignore"
    content = "\n".join(config.gitignore_lines) + "\n"
    gitignore_path.write_text(content, encoding="utf-8")
    logger.info("Created .gitignore")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def setup_vault(config_path: Path | None = None) -> None:
    """Run the full vault setup pipeline."""
    if config_path is None:
        config_path = PROJECT_ROOT / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found: {config_path} -- copy config.yaml.example and customise"
        )

    config = load_config(config_path)

    logger.info("=" * 60)
    logger.info("Vault Forge -- Setting up: %s", config.name)
    logger.info("Target: %s", config.path)
    logger.info("=" * 60)

    config.path.mkdir(parents=True, exist_ok=True)

    create_folders(config)
    copy_templates(config)
    copy_prompts(config)
    copy_starter_content(config)
    write_obsidian_config(config)
    install_plugins(config)
    init_git(config)

    logger.info("=" * 60)
    logger.info("Vault setup complete!")
    logger.info("Open Obsidian -> Open folder as vault -> %s", config.path)
    logger.info("=" * 60)


if __name__ == "__main__":
    setup_vault()
