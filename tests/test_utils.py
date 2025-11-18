from sync_settings_dotenv.utils import import_class_from_module


def test_import_class_from_path():
    model = import_class_from_module("tests.test_command")
    assert model.__name__ == "DummySettings"
