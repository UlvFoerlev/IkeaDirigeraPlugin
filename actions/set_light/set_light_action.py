from pathlib import Path
from urllib.parse import parse_qs, urlparse

from gi.repository import Adw, Gtk, Pango
from GtkHelper.GtkHelper import ComboRow, ScaleRow

from ..light_action import LightAction


class SetLightAction(LightAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def light(self):
        if not self.selected_light:
            return None

        return self.plugin_base.backend.lights_cache.get(self.selected_light)

    def on_key_down(self):
        # Initiate hub if not initiated yet
        if not self.plugin_base.backend.hub:
            self.plugin_base.backend.refresh_hub()

        # Initiate cache of lights, if not initiated yet
        if not self.plugin_base.backend.lights_cache:
            self.plugin_base.backend.load_lights()

        # If lights, and none selected, pick the first
        if not self.selected_light and self.lights:
            self.selected_light = self.lights[0].id

        print(self.light, self.active, self.active)
        if not self.light:
            return

        self.light.set_light(lamp_on=self.active)
        if self.active:
            self.light.set_light_level(light_level=self.light_level)
            self.light.set_color_temperature(color_temp=self.color_temperature)
            self.light.set_light_color(
                hue=self.light_color_hue, saturation=self.light_color_saturation
            )
