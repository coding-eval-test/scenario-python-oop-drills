import pytest

from plugins.loader import Settings, describe, load_exporter

pytestmark = pytest.mark.guard


def test_csv_exporter_joins_cells_and_rows():
    assert load_exporter("csv").export([[1, "a"], [2, "b"]]) == "1,a\n2,b"


def test_json_exporter_serialises_rows():
    assert load_exporter("json").export([[1, "a"]]) == '[[1, "a"]]'


def test_unknown_exporter_raises_value_error():
    with pytest.raises(ValueError):
        load_exporter("xml")


def test_describe_reads_the_default_settings():
    assert describe(Settings()) == "localhost:8080 debug=False"
