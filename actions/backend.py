from streamcontroller_plugin_tools import BackendBase
from pathlib import Path
from dirigera import Hub
from dirigera.devices.light import Light
from requests import ConnectionError


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


backend = Backend()
