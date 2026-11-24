"""Settings and exporters, wired by hand. Other code still uses this module."""
import json


class Settings:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.debug = False


class CsvExporter:
    def export(self, rows):
        return "\n".join(",".join(str(cell) for cell in row) for row in rows)


class JsonExporter:
    def export(self, rows):
        return json.dumps(rows)


def load_exporter(kind):
    if kind == "csv":
        return CsvExporter()
    if kind == "json":
        return JsonExporter()
    raise ValueError(f"unknown exporter: {kind}")


def describe(settings):
    return f"{settings.host}:{settings.port} debug={settings.debug}"
