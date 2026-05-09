from jinja2 import Environment

TEMPLATE = """{%- set target = trigger_target_lights | default({}, true) -%}
{%- set entities = target.entity_id if target is mapping and 'entity_id' in target else target -%}
{%- set raw_list = [entities] if entities is string else (entities if entities is sequence and entities is not mapping else []) -%}
{{ raw_list
   | reject('none')
   | reject('equalto', '')
   | unique
   | list }}"""


def render(**kwargs):
    env = Environment()
    return env.from_string(TEMPLATE).render(**kwargs)


def test_mapping_input():
    assert render(trigger_target_lights={"entity_id": ["light.a", "light.b"]}) == "['light.a', 'light.b']"


def test_string_input():
    assert render(trigger_target_lights="light.a") == "['light.a']"


def test_none_input():
    assert render(trigger_target_lights=None) == "[]"


def test_undefined_input():
    assert render() == "[]"


def test_removes_empty_and_duplicates():
    assert render(trigger_target_lights=["light.a", "", "light.a", None, "light.b"]) == "['light.a', 'light.b']"
