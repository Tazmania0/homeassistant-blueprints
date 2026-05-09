# Blueprints for Home Assistant
This repository contain various blueprints for Home Assistant.

Blueprints are used as templates for building automations really quickly.

## Included blueprint notes

### `dim_lights_based_on_sun_elevation.yaml`
- Core functionality: automatically adjusts light brightness based on current sun elevation between your configured rise/set elevation anchors.
- Supports optional automatic turn-on (when sun is setting) and turn-off (when sun has risen).
- Supports reverse/daylight behavior toggles and manual-change allowance thresholds.
- Supports transition smoothing through `transition_time`.
- Supports optional color temperature transitions from warm to cool (`min_color_temp_kelvin` → `max_color_temp_kelvin`) using the same sun-position curve.
- Supports optional weather-aware cooling through a `weather` entity (for example Home Assistant default Met.no). If no weather entity is set, color temperature follows only the sun curve.
- Automatically handles mixed light capabilities:
  - lights with color temperature support get `brightness + color_temp_kelvin`
  - lights without color temperature support get brightness updates only
