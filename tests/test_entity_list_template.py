from jinja2 import Environment

TEMPLATE = """{%- set target = target_lights | default({}, true) -%}
{%- set entities = target.entity_id if target is mapping else target -%}
{%- set entities = entities | default([], true) -%}
{{ [entities] if entities is string else entities }}"""


def render(target_lights):
    env = Environment()
    return env.from_string(TEMPLATE).render(target_lights=target_lights)


def test_mapping_input():
    assert render({"entity_id": ["light.a", "light.b"]}) == "['light.a', 'light.b']"


def test_list_input():
    assert render(["light.a", "light.b"]) == "['light.a', 'light.b']"


def test_string_input():
    assert render("light.a") == "['light.a']"


def test_none_input():
    assert render(None) == "[]"
