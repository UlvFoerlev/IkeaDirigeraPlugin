from .ikea_action_base import IkeaActionBase
from gi.repository import Adw, Gtk, Pango
from GtkHelper.GtkHelper import ComboRow, ScaleRow


class LightAction(IkeaActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self):
        base = super().get_config_rows()
        self.setup_select_light(base=base)

        return base

    def setup_select_light(self, base):
        self.dropdown_option = Gtk.ListStore.new([str])
        self.dropdown_name = Gtk.ListStore.new([str])
        self.mode_row = ComboRow(
            title=self.plugin_base.lm.get("action.light-action.select_light"),
            model=self.dropdown_name,
        )

        selected_light_index = 0

        self.plugin_base.backend.load_lights()

        self.dropdown_option.clear()
        for i, light in enumerate(self.lights):
            name = (
                light.attributes.custom_name
                if light.attributes.custom_name
                else f"Light {i}: {light.id}"
            )
            self.dropdown_option.append([light.id])
            self.dropdown_name.append([name])

            if light.id == self.selected_light:
                selected_light_index = i

        self.mode_cell_renderer = Gtk.CellRendererText(
            ellipsize=Pango.EllipsizeMode.END, max_width_chars=60
        )
        self.mode_row.combo_box.pack_start(self.mode_cell_renderer, True)
        self.mode_row.combo_box.add_attribute(self.mode_cell_renderer, "text", 0)

        self.mode_row.combo_box.set_active(selected_light_index)

        # Connect entries
        self.mode_row.combo_box.connect("changed", self.on_select_light)

        base.append(self.mode_row)

    @property
    def lights(self):
        return self.plugin_base.backend.lights

    @property
    def selected_light(self) -> str:
        return self._get_property(key="selected_light", default=None)

    @selected_light.setter
    def selected_light(self, value: str):
        self._set_property(key="selected_light", value=value)

    @property
    def active(self) -> bool:
        return self._get_property(key="active", default=True, enforce_type=bool)

    @active.setter
    def active(self, value: bool):
        self._set_property(key="active", value=value)

    @property
    def light_level(self) -> int:
        return self._get_property(key="light_level", default=100, enforce_type=int)

    @light_level.setter
    def light_level(self, level: int):
        if 1 < level > 100:
            raise ValueError(
                f"Parameter 'level' must be between 1 and 100, not {level}."
            )

        self._set_property(key="light_level", value=level)

    @property
    def color_temperature(self) -> int:
        return self._get_property(
            key="color_temperature", default=100, enforce_type=int
        )

    @color_temperature.setter
    def color_temperature(self, temperature: int):
        self._set_property(key="color_temperature", value=temperature)

    @property
    def light_color_hue(self) -> int:
        return self._get_property(key="light_color_hue", default=100, enforce_type=int)

    @light_color_hue.setter
    def light_color_hue(self, hue: int):
        if hue < 0 or hue > 360:
            raise ValueError(f"Parameter 'hue' must be between 0 and 360, not {hue}.")

        self._set_property(key="light_color_hue", value=hue)

    @property
    def light_color_saturation(self) -> float:
        return self._get_property(
            key="light_color_saturation", default=1, enforce_type=float
        )

    @light_color_saturation.setter
    def light_color_saturation(self, saturation: float):
        if saturation < 0 or saturation > 1:
            raise ValueError(
                f"Parameter 'saturation' must be between 0 and 1, not {saturation}."
            )

        self._set_property(key="light_color_saturation", value=saturation)

    def on_select_light(self, option):
        pass
