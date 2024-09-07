from .set_light_action import SetLightAction

from gi.repository import Adw, Gtk, Pango
from GtkHelper.GtkHelper import ComboRow, ScaleRow


class SetLightRGBAction(SetLightAction):
    def _setup_settings(self, base):
        self.setup_red_slider(base=base)
        self.setup_green_slider(base=base)
        self.setup_blue_slider(base=base)

    def setup_red_slider(self, base):
        self.color_red_slider = ScaleRow(
            title=self.plugin_base.lm.get("action.set-light.red"),
            value=self.color_red,
            min=0,
            max=255,
            step=1,
            text_left="0",
            text_right="255",
        )
        self.color_red_slider.scale.set_draw_value(True)

        self.color_red_slider.adjustment.connect(
            "value-changed", self.on_color_red_slider_change
        )

        base.append(self.color_red_slider)

    def setup_green_slider(self, base):
        self.color_green_slider = ScaleRow(
            title=self.plugin_base.lm.get("action.set-light.green"),
            value=self.color_green,
            min=0,
            max=255,
            step=1,
            text_left="0",
            text_right="255",
        )
        self.color_green_slider.scale.set_draw_value(True)

        self.color_green_slider.adjustment.connect(
            "value-changed", self.on_color_green_slider_change
        )

        base.append(self.color_green_slider)

    def setup_blue_slider(self, base):
        self.color_blue_slider = ScaleRow(
            title=self.plugin_base.lm.get("action.set-light.blue"),
            value=self.color_blue,
            min=0,
            max=255,
            step=1,
            text_left="0",
            text_right="255",
        )
        self.color_blue_slider.scale.set_draw_value(True)

        self.color_blue_slider.adjustment.connect(
            "value-changed", self.on_color_blue_slider_change
        )

        base.append(self.color_blue_slider)

    @property
    def color_red(self) -> int:
        return self._get_property(key="color_red", default=255, enforce_type=int)

    @color_red.setter
    def color_red(self, value: int):
        if value < 0 or value > 360:
            raise ValueError(
                f"Parameter 'value' must be between 0 and 255, not {value}."
            )

        self._set_property(key="color_red", value=value)

    @property
    def color_green(self) -> int:
        return self._get_property(key="color_green", default=255, enforce_type=int)

    @color_green.setter
    def color_green(self, value: int):
        if value < 0 or value > 360:
            raise ValueError(
                f"Parameter 'value' must be between 0 and 255, not {value}."
            )

        self._set_property(key="color_green", value=value)

    @property
    def color_blue(self) -> int:
        return self._get_property(key="color_blue", default=255, enforce_type=int)

    @color_blue.setter
    def color_blue(self, value: int):
        if value < 0 or value > 360:
            raise ValueError(
                f"Parameter 'value' must be between 0 and 255, not {value}."
            )

        self._set_property(key="color_blue", value=value)

    def _calculate_hue_from_rgb(self, r: float, g: float, b: float) -> int:
        hue = 0.0

        if r == g == b:
            return 0

        if r >= g and r >= b:
            hue = (g - b) / (r - min([r, g, b]))
        if g >= r and g >= b:
            hue = 2.0 + (b - r) / (g - min([r, g, b]))
        if b >= g and b >= r:
            hue = 4.0 + (r - g) / (b - min([r, g, b]))

        return int(hue * 60) % 360

    def _calculate_saturation_from_rgb(self, r: float, g: float, b: float) -> float:
        delta = max([r, g, b]) - min([r, g, b])
        if delta == 0:
            return 0

        light_level = self._calculate_light_level_from_rgb(r, g, b)

        dividend = 1 - abs(2 * light_level - 1)

        if dividend == 0:
            return 1

        return delta / dividend

    def _calculate_light_level_from_rgb(self, r: float, g: float, b: float) -> int:
        return int(max([r, g, b]) + min([r, g, b]) / 2)

    def on_color_red_slider_change(self, entry):
        self.color_red = int(entry.get_value())

    def on_color_green_slider_change(self, entry):
        self.color_green = int(entry.get_value())

    def on_color_blue_slider_change(self, entry):
        self.color_blue = int(entry.get_value())

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

        R = self.color_red / 255
        G = self.color_green / 255
        B = self.color_blue / 255

        hue = self._calculate_hue_from_rgb(R, G, B)
        saturation = self._calculate_saturation_from_rgb(R, G, B)
        light_level = self._calculate_light_level_from_rgb(R, G, B)

        self.plugin_base.backend.set_light_state(
            light=self.light,
            active=self.active,
            level=light_level,
            hue=hue,
            saturation=saturation,
        )
