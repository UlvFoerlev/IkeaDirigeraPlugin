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

        return self.plugin_base.backend.cached_lights.get(self.selected_light)

    def on_key_down(self):
        if not self.light:
            return

        self.light.set_light(lamp_on=self.active)
        if self.active:
            self.light.set_light_level(ligth_level=self.light_level)
            self.light.set_color_temperature(color_temp=self.color_temperature)
            self.light.set_light_color(
                hue=self.light_color_hue, saturation=self.light_color_saturation
            )
