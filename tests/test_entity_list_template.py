from jinja2 import Environment

TEMPLATE = """{%- set target = target_lights | default({}, true) -%}
{%- set entities = target.entity_id if target is mapping and 'entity_id' in target else target -%}
{%- set raw_list = [entities] if entities is string else (entities if entities is sequence and entities is not mapping else []) -%}
{%- set expanded = namespace(entities=[]) -%}
{%- for e in raw_list | reject('none') | reject('equalto', '') -%}
  {%- set children = state_attr(e, 'entity_id') -%}
  {%- if children is sequence and children is not string -%}
    {%- set expanded.entities = expanded.entities + children -%}
  {%- else -%}
    {%- set expanded.entities = expanded.entities + [e] -%}
  {%- endif -%}
{%- endfor -%}
{{ expanded.entities | unique | list }}"""


ENTITY_ATTRIBUTES = {
    "light.group": {"entity_id": ["light.a", "light.b"]},
    "light.group_with_duplicate": {"entity_id": ["light.a", "light.c", "light.a"]},
}


def render(target_lights):
    env = Environment()
    env.globals["state_attr"] = lambda entity_id, attr: ENTITY_ATTRIBUTES.get(entity_id, {}).get(attr)
    return env.from_string(TEMPLATE).render(target_lights=target_lights)


def test_mapping_input():
    assert render({"entity_id": ["light.a", "light.b"]}) == "['light.a', 'light.b']"


def test_list_input():
    assert render(["light.a", "light.b"]) == "['light.a', 'light.b']"


def test_string_input():
    assert render("light.a") == "['light.a']"


def test_none_input():
    assert render(None) == "[]"


def test_expands_light_group_entities():
    assert render("light.group") == "['light.a', 'light.b']"


def test_deduplicates_expanded_group_entities():
    assert render(["light.group_with_duplicate", "light.c"]) == "['light.a', 'light.c']"
