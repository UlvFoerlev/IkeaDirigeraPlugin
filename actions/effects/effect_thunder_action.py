from gi.repository import Gtk
from GtkHelper.GtkHelper import ScaleRow

from ..light_action import LightAction


class EffectThunderAction(LightAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def light(self):
        if not self.selected_light:
            return None

        return self.plugin_base.backend.lights_cache.get(self.selected_light)

    def get_config_rows(self):
        base = super().get_config_rows()

        return base

    def on_key_down(self):
        # Initiate hub if not initiated yet
        if not self.plugin_base.backend.hub:
            self.refresh_hub()

        # Initiate cache of lights, if not initiated yet
        if not self.plugin_base.backend.lights_cache:
            self.plugin_base.backend.load_lights()

        # If lights, and none selected, pick the first
        if not self.selected_light and self.lights:
            self.selected_light = self.lights[0].id

        if not self.light:
            return

        self.plugin_base.backend.thunder_effect()
