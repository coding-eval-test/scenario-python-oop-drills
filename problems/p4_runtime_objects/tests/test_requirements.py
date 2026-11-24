from types import SimpleNamespace

import pytest

from plugins.loader import Settings
from plugins.runtime import (
    Registry,
    apply_overrides,
    attach_method,
    patch_class,
    read_setting,
)


class Greeter:
    def __init__(self, name):
        self.name = name


def shout(self):
    return self.name.upper() + "!"


def test_apply_overrides_updates_existing_attributes():
    settings = Settings()
    apply_overrides(settings, {"port": 9090, "debug": True})
    assert (settings.host, settings.port, settings.debug) == ("localhost", 9090, True)


def test_apply_overrides_reports_and_skips_unknown_names():
    settings = Settings()
    rejected = apply_overrides(settings, {"timeout": 30, "port": 9090, "colour": "red"})
    assert rejected == ["colour", "timeout"]
    assert settings.port == 9090
    assert not hasattr(settings, "timeout")
    assert not hasattr(settings, "colour")


def test_apply_overrides_returns_an_empty_list_when_all_names_exist():
    assert apply_overrides(Settings(), {"host": "example.org"}) == []


def test_read_setting_follows_a_dotted_path():
    config = SimpleNamespace(database=SimpleNamespace(primary=SimpleNamespace(port=5432)))
    assert read_setting(config, "database.primary.port") == 5432
    assert read_setting(Settings(), "host") == "localhost"


def test_read_setting_returns_the_default_when_any_step_is_missing():
    config = SimpleNamespace(database=SimpleNamespace(primary=SimpleNamespace(port=5432)))
    assert read_setting(config, "database.replica.port", default=0) == 0
    assert read_setting(config, "cache") is None


def test_attach_method_binds_the_function_to_that_object():
    greeter = Greeter("dana")
    attach_method(greeter, "shout", shout)
    assert greeter.shout() == "DANA!"


def test_attach_method_leaves_the_class_and_other_objects_alone():
    first, second = Greeter("dana"), Greeter("lee")
    attach_method(first, "shout", shout)
    assert not hasattr(second, "shout")
    assert not hasattr(Greeter, "shout")


def test_patch_class_reaches_objects_that_already_exist():
    class Robot:
        def __init__(self, name):
            self.name = name

    existing = Robot("r2")
    patch_class(Robot, "shout", shout)
    assert existing.shout() == "R2!"
    assert Robot("c3").shout() == "C3!"


def test_registry_registers_and_creates_by_name():
    registry = Registry()

    @registry.register("greeter")
    class LocalGreeter(Greeter):
        pass

    assert LocalGreeter.__name__ == "LocalGreeter"
    created = registry.create("greeter", "dana")
    assert type(created) is LocalGreeter
    assert created.name == "dana"
    assert registry.names() == ["greeter"]

    @registry.register("crate")
    class Crate:
        def __init__(self, label, size="small"):
            self.label = label
            self.size = size

    crate = registry.create("crate", "apples", size="large")
    assert (crate.label, crate.size) == ("apples", "large")
    assert registry.names() == ["crate", "greeter"]


def test_registry_rejects_unknown_and_duplicate_names():
    registry = Registry()
    registry.register("greeter")(Greeter)
    with pytest.raises(KeyError):
        registry.create("robot")
    with pytest.raises(ValueError):
        registry.register("greeter")(Greeter)
    assert Registry().names() == []
