"""Utilities for loading nqdc plug-in functionality."""

from typing import Dict, List, Any

import importlib_metadata


def get_plugin_actions() -> Dict[str, List[Any]]:
    """Load entry points from all nqdc plugins.

    See https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    """
    all_actions: Dict[str, List[Any]] = {
        "pipeline_steps": [],
        "commands": [],
    }
    for entry_point in importlib_metadata.entry_points().select(
        group="nqdc.plugin_actions"
    ):
        plugin_actions = entry_point.load()()
        for kind, steps in all_actions.items():
            steps.extend(plugin_actions.get(kind, []))
    return all_actions
