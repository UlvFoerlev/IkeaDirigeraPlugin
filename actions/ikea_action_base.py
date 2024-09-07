from src.backend.PluginManager.ActionBase import ActionBase
from typing import Any
from gi.repository import Adw
import socket


class IkeaActionBase(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_property(
        self, key: str, default: Any = None, enforce_type: type | None = None
    ) -> Any:
        settings = self.get_settings()
        value = settings.get(key, default)

        if enforce_type and isinstance(value, enforce_type) is False:
            value = default

        return value

    def _set_property(self, key: str, value: Any) -> None:
        settings = self.get_settings()
        settings[key] = value
        self.set_settings(settings)

    def setup_hub_info_input(self, base):
        self.ip_input = Adw.EntryRow(
            title=self.plugin_base.lm.get("action.hub_info.ip")
        )
        self.ip_input.set_text(self.hub_ip)

        self.token_input = Adw.EntryRow(
            title=self.plugin_base.lm.get("action.hub_info.token")
        )
        self.token_input.set_text(self.hub_token)

        self.ip_input.connect("notify::text", self.on_ip_change)
        self.token_input.connect("notify::text", self.on_token_change)

        base.append(self.ip_input)
        base.append(self.token_input)

    def get_config_rows(self):
        if not self.plugin_base.backend.hub:
            self.refresh_hub()

        base = super().get_config_rows()
        self.setup_hub_info_input(base=base)

        return base

    @property
    def hub_ip(self) -> str:
        return self._get_property(key="hub_ip", default="", enforce_type=str)

    @hub_ip.setter
    def hub_ip(self, ip: str) -> None:
        if not isinstance(ip, str):
            raise TypeError(f"Type of parameter 'ip' must be 'str' not '{type(ip)}'")

        self._set_property(key="hub_ip", value=ip)

    @property
    def hub_token(self) -> str:
        return self._get_property(key="hub_token", default="", enforce_type=str)

    @hub_token.setter
    def hub_token(self, token: str) -> None:
        if not isinstance(token, str):
            raise TypeError(
                f"Type of parameter 'token' must be 'str' not '{type(token)}'"
            )

        self._set_property(key="hub_token", value=token)

    def setup_hub(self, ip: str, token: str):
        self.plugin_base.backend.setup_hub(ip=ip, token=token)

    def on_ip_change(self, entry, _):
        self.hub_ip = entry.get_text()

        if self.hub_ip and self.hub_token:
            self.setup_hub(ip=self.hub_ip, token=self.hub_token)

    def on_token_change(self, entry, _):
        self.hub_token = entry.get_text()

    def valid_ip(self, ip: str) -> bool:
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def refresh_hub(self):
        if self.hub_ip and self.valid_ip(self.hub_ip) and self.hub_token:
            self.setup_hub(ip=self.hub_ip, token=self.hub_token)
