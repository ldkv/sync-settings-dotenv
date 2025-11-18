from datetime import datetime
from enum import Enum
from pathlib import Path
from unittest.mock import MagicMock, patch

from pydantic import Field
from pydantic_settings import BaseSettings

from sync_settings_dotenv.main import import_class_from_module, sync_settings_dotenv


class ENV(Enum):
    dev = "DeV"
    ProD = "prod"


class DummySettings(BaseSettings):
    foo: str = "bar"
    baz: int = 42
    env: ENV = ENV.dev
    dt: datetime = datetime(2024, 1, 1, 12, 0, 0)
    null_value: str | None = None
    excluded_field: str = Field(default="should not appear", exclude=True)

    @classmethod
    def assert_env_content(cls, content: str):
        assert "FOO=bar\n" in content
        assert "BAZ=42\n" in content
        assert "ENV=DeV\n" in content
        assert "DT=2024-01-01T12:00:00\n" in content
        assert "NULL_VALUE=\n" in content
        assert "EXCLUDED_FIELD" not in content


def test_import_class_from_path():
    model = import_class_from_module("tests.test_command")
    assert model.__name__ == "DummySettings"


@patch("sync_settings_dotenv.utils.shutil.copy")
def test_sync_settings_dotenv(mock_shutil: "MagicMock", tmp_path: Path):
    env_path = tmp_path / ".env"
    sync_settings_dotenv(module_path="tests.test_command", env_path=env_path)
    content = env_path.read_text()
    mock_shutil.assert_not_called()
    DummySettings.assert_env_content(content)

    # Call again without any changes; no overwrite should happen
    sync_settings_dotenv(module_path="tests.test_command", env_path=env_path)
    mock_shutil.assert_not_called()
    new_content = env_path.read_text()
    assert new_content == content
