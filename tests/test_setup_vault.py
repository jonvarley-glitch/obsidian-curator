"""Unit tests for setup_vault.

Tests run against a temporary vault directory (`tmp_path`) and never touch
the user's real vault. Network-dependent steps (plugin downloads) are not
exercised here; that is covered by `--skip-plugins` integration runs.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import setup_vault as sv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REAL_CONFIG = PROJECT_ROOT / "config.yaml"


def _write_config(path: Path, vault_path: Path) -> Path:
    """Write a minimal but valid config.yaml at `path` pointing at `vault_path`."""
    raw = yaml.safe_load(REAL_CONFIG.read_text(encoding="utf-8"))
    raw["vault"]["path"] = str(vault_path)
    config_path = path / "config.yaml"
    config_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return config_path


# ---------------------------------------------------------------------------
# load_config / validate_config
# ---------------------------------------------------------------------------

def test_load_real_config_returns_populated_struct() -> None:
    config = sv.load_config(REAL_CONFIG)
    assert config.name
    assert config.path.is_absolute()
    assert config.folders, "folders list should not be empty"
    assert config.plugins, "plugins list should not be empty"
    plugin_ids = {p.id for p in config.plugins}
    assert "obsidian-tasks-plugin" in plugin_ids
    assert "obsidian-excalidraw-plugin" in plugin_ids


def test_load_config_missing_vault_raises(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("folders: []\n", encoding="utf-8")
    with pytest.raises(sv.ConfigError, match="vault"):
        sv.load_config(config_path)


def test_load_config_missing_vault_path_raises(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "vault:\n  name: Test\nfolders: []\n",
        encoding="utf-8",
    )
    with pytest.raises(sv.ConfigError, match="vault.path"):
        sv.load_config(config_path)


def test_load_config_bad_plugin_repo_raises(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "vault:\n  name: Test\n  path: ./vault\n"
        "plugins:\n  - id: foo\n    repo: not-a-repo\n",
        encoding="utf-8",
    )
    with pytest.raises(sv.ConfigError, match="owner/name"):
        sv.load_config(config_path)


def test_validate_config_clean(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    issues = sv.validate_config(config)
    assert issues == []


def test_validate_config_detects_duplicate_plugin_ids(tmp_path: Path) -> None:
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=["a"],
        plugins=[
            sv.PluginSpec(id="dup", repo="o/n"),
            sv.PluginSpec(id="dup", repo="o/m"),
        ],
        core_plugins={},
        app_settings={"a": 1},
        community_plugin_ids=["dup", "dup"],
    )
    issues = sv.validate_config(config, templates_dir=tmp_path)
    assert any("duplicate" in i for i in issues)


def test_validate_config_warns_on_empty_folders(tmp_path: Path) -> None:
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=[],
        plugins=[sv.PluginSpec(id="p", repo="o/n")],
        core_plugins={},
        app_settings={"a": 1},
        community_plugin_ids=["p"],
    )
    issues = sv.validate_config(config, templates_dir=tmp_path)
    assert any("folders" in i for i in issues)


def test_validate_config_warns_on_empty_plugins(tmp_path: Path) -> None:
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=["a"],
        plugins=[],
        core_plugins={},
        app_settings={"a": 1},
        community_plugin_ids=[],
    )
    issues = sv.validate_config(config, templates_dir=tmp_path)
    assert any("plugins" in i for i in issues)


def test_validate_config_warns_on_empty_app_settings(tmp_path: Path) -> None:
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=["a"],
        plugins=[sv.PluginSpec(id="p", repo="o/n")],
        core_plugins={},
        app_settings={},
        community_plugin_ids=["p"],
    )
    issues = sv.validate_config(config, templates_dir=tmp_path)
    assert any("app_settings" in i for i in issues)


def test_validate_config_rejects_bad_template_type(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "nope.md").write_text(
        "---\ntype: not_a_real_type\n---\n# Test\n", encoding="utf-8",
    )
    (templates / "good.md").write_text(
        "---\ntype: meeting\n---\n# OK\n", encoding="utf-8",
    )
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=["a"],
        plugins=[sv.PluginSpec(id="p", repo="o/n")],
        core_plugins={},
        app_settings={"a": 1},
        community_plugin_ids=["p"],
        note_types=["meeting"],
    )
    issues = sv.validate_config(config, templates_dir=templates)
    assert any("not_a_real_type" in i for i in issues)
    assert not any("good.md" in i for i in issues)


def test_validate_config_flags_missing_type_in_template(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "no-frontmatter.md").write_text(
        "# Just a heading, no frontmatter\n", encoding="utf-8",
    )
    config = sv.VaultConfig(
        name="x",
        path=Path("/tmp/x"),
        folders=["a"],
        plugins=[sv.PluginSpec(id="p", repo="o/n")],
        core_plugins={},
        app_settings={"a": 1},
        community_plugin_ids=["p"],
        note_types=["meeting"],
    )
    issues = sv.validate_config(config, templates_dir=templates)
    assert any("missing literal 'type:'" in i for i in issues)


def test_scan_template_types_skips_templater_placeholder(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "dynamic.md").write_text(
        "<%* const t = 'meeting'; -%>\n---\ntype: <% t %>\n---\n",
        encoding="utf-8",
    )
    types = sv.scan_template_types(templates)
    assert types["dynamic.md"] is None


def test_real_templates_pass_type_validation() -> None:
    """The shipped templates must all declare a literal type in note_types."""
    config = sv.load_config(REAL_CONFIG)
    issues = sv.validate_config(config)
    type_issues = [i for i in issues if "templates/" in i]
    assert type_issues == [], f"shipped templates have type issues: {type_issues}"


# ---------------------------------------------------------------------------
# Folder + content + base + kanban copy steps
# ---------------------------------------------------------------------------

def test_create_folders_produces_full_tree(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.create_folders(config)
    for folder in config.folders:
        assert (config.path / folder).is_dir()


def test_copy_templates_copies_every_md_file(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.copy_templates(config)
    src = sorted((PROJECT_ROOT / "templates").glob("*.md"))
    dest = sorted((config.path / "Templates").glob("*.md"))
    assert {f.name for f in src} == {f.name for f in dest}
    assert len(src) > 0


def test_copy_prompts_copies_every_md_file(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.copy_prompts(config)
    src = sorted((PROJECT_ROOT / "prompts").glob("*.md"))
    dest = sorted((config.path / "Prompts").glob("*.md"))
    assert {f.name for f in src} == {f.name for f in dest}


def test_copy_bases_copies_every_base_file(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.copy_bases(config)
    src = sorted((PROJECT_ROOT / "content" / "bases").glob("*.base"))
    dest = sorted((config.path / "Bases").glob("*.base"))
    assert {f.name for f in src} == {f.name for f in dest}
    assert len(src) >= 4


def test_copy_bases_is_idempotent(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.copy_bases(config)
    customised = config.path / "Bases" / "Customers.base"
    customised.write_text("# user-edited\n", encoding="utf-8")
    sv.copy_bases(config)
    assert customised.read_text(encoding="utf-8") == "# user-edited\n"


def test_copy_kanban_lands_under_13_tasks(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    sv.copy_kanban(config)
    board = config.path / "13-Tasks" / "Task Board.md"
    assert board.exists()
    content = board.read_text(encoding="utf-8")
    assert "kanban-plugin" in content


def test_copy_starter_content_skips_task_board(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.copy_starter_content(config)
    assert (config.path / "Home.md").exists()
    assert not (config.path / "Task Board.md").exists(), (
        "Task Board.md must not be copied to vault root"
    )


# ---------------------------------------------------------------------------
# Plugin configs
# ---------------------------------------------------------------------------

def test_write_plugin_configs_copies_data_json(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.write_plugin_configs(config)
    for src in (PROJECT_ROOT / "obsidian_config" / "plugins").glob("*/data.json"):
        plugin_id = src.parent.name
        dest = config.path / ".obsidian" / "plugins" / plugin_id / "data.json"
        assert dest.exists(), f"missing {dest}"


def test_write_plugin_configs_is_idempotent(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.write_plugin_configs(config)
    target = config.path / ".obsidian" / "plugins" / "homepage" / "data.json"
    target.write_text("{\"user\": true}\n", encoding="utf-8")
    sv.write_plugin_configs(config)
    assert target.read_text(encoding="utf-8") == "{\"user\": true}\n"


# ---------------------------------------------------------------------------
# write_vault_gitignore
# ---------------------------------------------------------------------------

def test_write_vault_gitignore_writes_every_line(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.write_vault_gitignore(config)
    gi = (config.path / ".gitignore").read_text(encoding="utf-8")
    for line in config.gitignore_lines:
        assert line in gi


# ---------------------------------------------------------------------------
# write_obsidian_config -- app.json merge + idempotency
# ---------------------------------------------------------------------------

def test_write_obsidian_config_merges_app_settings(tmp_path: Path) -> None:
    import json
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.write_obsidian_config(config)
    written = json.loads(
        (config.path / ".obsidian" / "app.json").read_text(encoding="utf-8"),
    )
    for key, value in config.app_settings.items():
        assert written[key] == value


def test_write_obsidian_config_preserves_user_top_level_jsons(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    obsidian_dir = config.path / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    user_hotkeys = obsidian_dir / "hotkeys.json"
    user_hotkeys.write_text("{\"user\": true}\n", encoding="utf-8")
    sv.write_obsidian_config(config)
    assert user_hotkeys.read_text(encoding="utf-8") == "{\"user\": true}\n"


def test_write_obsidian_config_rewrites_app_json_each_run(tmp_path: Path) -> None:
    """app.json is config-derived: re-running propagates config changes."""
    import json
    config_path = _write_config(tmp_path, tmp_path / "vault")
    config = sv.load_config(config_path)
    config.path.mkdir(parents=True, exist_ok=True)
    sv.write_obsidian_config(config)
    config.app_settings["__test_key__"] = "test_value"
    sv.write_obsidian_config(config)
    written = json.loads(
        (config.path / ".obsidian" / "app.json").read_text(encoding="utf-8"),
    )
    assert written.get("__test_key__") == "test_value"


# ---------------------------------------------------------------------------
# main() entrypoint
# ---------------------------------------------------------------------------

def test_main_validate_returns_zero(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path, tmp_path / "vault")
    rc = sv.main(["--validate", "--config", str(config_path)])
    assert rc == 0


def test_main_validate_bad_config_returns_one(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("not: vault\n", encoding="utf-8")
    rc = sv.main(["--validate", "--config", str(config_path)])
    assert rc == 1


def test_main_validate_missing_config_returns_one(tmp_path: Path) -> None:
    rc = sv.main(["--validate", "--config", str(tmp_path / "nope.yaml")])
    assert rc == 1


# ---------------------------------------------------------------------------
# End-to-end with --skip-plugins (no network)
# ---------------------------------------------------------------------------

def test_setup_vault_skip_plugins_end_to_end(tmp_path: Path) -> None:
    import json
    config_path = _write_config(tmp_path, tmp_path / "vault")
    sv.setup_vault(config_path=config_path, skip_plugins=True)
    vault = tmp_path / "vault"
    assert (vault / "Home.md").exists()
    assert (vault / "Templates" / "meeting.md").exists()
    assert (vault / "Templates" / "system.md").exists()
    assert (vault / "Bases" / "Customers.base").exists()
    assert (vault / "Bases" / "Systems.base").exists()
    assert (vault / "13-Tasks" / "Task Board.md").exists()
    assert (vault / "Daily").is_dir()
    assert (vault / ".obsidian" / "app.json").exists()
    assert (vault / ".gitignore").exists()
    app_settings = json.loads(
        (vault / ".obsidian" / "app.json").read_text(encoding="utf-8"),
    )
    assert app_settings.get("attachmentFolderPath") == "Assets"
    assert app_settings.get("newFileFolderPath") == "00-Inbox"
