from jinja2 import Environment

TEMPLATE = """{{ (trigger_target_lights.entity_id if trigger_target_lights is mapping else trigger_target_lights)
   | default([], true) }}"""


def render(**kwargs):
    env = Environment()
    return env.from_string(TEMPLATE).render(**kwargs)


def test_mapping_input():
    assert render(trigger_target_lights={"entity_id": ["light.a", "light.b"]}) == "['light.a', 'light.b']"


def test_string_input():
    assert render(trigger_target_lights="light.a") == "light.a"


def test_none_input():
    assert render(trigger_target_lights=None) == "[]"


def test_undefined_input():
    assert render() == "[]"
