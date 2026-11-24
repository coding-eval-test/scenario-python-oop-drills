# P4 — Runtime object manipulation

**Suggested time:** 15 minutes · **Worth:** 20 points

## Context

`plugins/loader.py` wires settings and exporters by hand: every attribute and every
class is spelled out in code. Operations wants to change a live object from a
dictionary of overrides, bolt behavior onto objects that already exist, and look
classes up by name. `plugins/runtime.py` holds placeholders for the helpers that will
do it. None of them may assume anything about the objects they are handed.

## Requirements

1. `apply_overrides(target, overrides)` sets each name in the `overrides` dictionary
   on `target`, but only where `target` already has an attribute of that name. Names
   it does not have are left unset and returned as an alphabetically sorted list
   (an empty list when every name was applied).
2. `read_setting(target, dotted_path, default=None)` follows a path such as
   `"database.primary.port"` one attribute at a time and returns what it finds, or
   `default` as soon as any step is missing.
3. `attach_method(target, name, function)` makes `function` callable as
   `target.name()`, receiving `target` as its first argument. Only that one object
   gains it — its class and every other object of that class are untouched.
4. `patch_class(cls, name, function)` makes `function` callable as a method on every
   object of `cls`, including objects created before the call.
5. `Registry` keeps its own name-to-class table; two registries share nothing.
   - `registry.register(name)` is used as a class decorator. It records the class
     under `name` and hands the class back unchanged. Registering a name twice raises
     `ValueError`.
   - `registry.create(name, *args, **kwargs)` builds an object of the class recorded
     under `name`, passing the arguments through. An unknown name raises `KeyError`.
   - `registry.names()` returns the recorded names, alphabetically sorted.
6. Everything in `plugins/loader.py` must keep working, unchanged.

## Example

```python
settings = Settings()
print(apply_overrides(settings, {"port": 9090, "timeout": 30}))  # ['timeout']
print(settings.port)                                              # 9090

registry = Registry()

@registry.register("csv")
class Csv:
    ...

print(registry.names())  # ['csv']
```

## Running the tests

From this folder: `python -m pytest`. `tests/test_requirements.py` is what scores;
`tests/test_existing.py` covers behavior that already works and must keep working.
