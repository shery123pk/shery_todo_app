"""Pytest configuration and fixtures for todo CLI tests."""

import json
import sys
from pathlib import Path
from typing import Generator

import pytest

# Add cli directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_tasks_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide isolated tasks.json file for each test.

    Args:
        tmp_path: Pytest temporary directory fixture

    Yields:
        Path to temporary tasks.json file
    """
    tasks_file = tmp_path / "tasks.json"
    yield tasks_file
    # Cleanup after test
    if tasks_file.exists():
        tasks_file.unlink()


@pytest.fixture
def sample_tasks_data() -> dict:
    """Provide sample tasks data for testing.

    Returns:
        Dictionary with next_id and sample tasks
    """
    return {
        "next_id": 4,
        "tasks": [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
            },
            {
                "id": 2,
                "title": "Call dentist",
                "description": "",
                "completed": False,
            },
            {
                "id": 3,
                "title": "Finish report",
                "description": "Submit by Friday",
                "completed": True,
            },
        ],
    }


@pytest.fixture
def corrupted_json_file(tmp_path: Path) -> Path:
    """Provide a corrupted JSON file for error handling tests.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to corrupted JSON file
    """
    corrupted_file = tmp_path / "corrupted.json"
    corrupted_file.write_text("{ invalid json content }")
    return corrupted_file
