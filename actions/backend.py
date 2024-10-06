from typing import Any

from dirigera import Hub
from dirigera.devices.light import Light
from requests import ConnectionError
from streamcontroller_plugin_tools import BackendBase
from time import sleep


def clamp(val: Any, minimum: Any, maximum: any):
    return max(min(val, maximum), minimum)


class Backend(BackendBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hub: Hub | None = None

        self.lights_cache: dict[str, Light] = {}

    def setup_hub(self, ip: str, token: str) -> Hub:
        hub = Hub(token=token, ip_address=ip)

        self.hub = hub
        self.load_lights()
        return self.hub

    def reset_hub(self):
        self.hub = None

    def load_lights(self):
        self.lights_cache = {x.id: x for x in self.lights}

    @property
    def lights(self) -> list[Light]:
        if not self.hub:
            return []

        try:
            return self.hub.get_lights()
        except ConnectionError:
            self.reset_hub()
            return []

    def _alter_light_state(
        self,
        light: Light,
        level: int | None = None,
        temperature: int | None = None,
        hue: int | None = None,
        saturation: float | None = None,
    ):
        # if temperature is not None:
        #     temp_min = light.attributes.color_temperature_min
        #     temp_max = light.attributes.color_temperature_max

        #     if temp_min > temp_max:
        #         temp_min, temp_max = temp_max, temp_min

        #     light.set_color_temperature(
        #         color_temp=clamp(temperature, temp_min, temp_max)
        #     )

        if hue is not None or saturation is not None:
            new_hue = hue if hue is not None else light.attributes.color_hue
            new_hue = clamp(new_hue, 0, 360)
            new_saturation = (
                saturation
                if saturation is not None
                else light.attributes.color_saturation
            )
            new_saturation = clamp(new_saturation, 0.0, 1.0)

            light.set_light_color(hue=new_hue, saturation=new_saturation)

        if level:
            light.set_light_level(clamp(level, 1, 100))

    def set_light_state(
        self,
        light: Light,
        active: bool = True,
        level: int | None = None,
        temperature: int | None = None,
        hue: int | None = None,
        saturation: float | None = None,
        fade_in: int = 0,
    ):
        if light.attributes.is_on != active:
            light.set_light(lamp_on=active)

        if active is False:
            return

        self._alter_light_state(
            light=light,
            level=level,
            temperature=temperature,
            hue=hue,
            saturation=saturation,
        )

    def thunder_effect(self, light: Light):
        prev_state = {
            "active": light.attributes.is_on,
            "level": light.attributes.light_level,
            "temperature": light.attributes.color_temperature,
            "hue": light.attributes.color_hue,
            "saturation": light.attributes.color_saturation,
        }

        new_state = {
            "active": True,
            "level": 100,
            "temperature": 0,
            "hue": 0,
            "saturation": 0.0,
        }

        self.set_light_state(light=light, **new_state)
        sleep(0.15)
        self.set_light_state(light=light, **prev_state)
        sleep(0.1)
        self.set_light_state(light=light, **new_state)
        sleep(0.15)
        self.set_light_state(light=light, **prev_state)


backend = Backend()
