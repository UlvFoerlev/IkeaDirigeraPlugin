# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from pathlib import Path

from .actions.set_light.set_light_action import SetLightAction
from .actions.set_light.set_light_action_rgb import SetLightRGBAction
from .actions.effects.effect_thunder_action import EffectThunderAction


# Wiki
# https://core447.com/streamcontroller/docs/latest/


class PluginYoutubePlaylist(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        self.setup_backend()
        self.setup_actions()

        # Register plugin
        self.register(
            plugin_name="Ikea Dirigera Controller",
            github_repo="https://github.com/UlvFoerlev/IkeaDirigeraPlugin",
            plugin_version="1.0.0",
            app_version="1.5.0-beta",
        )

    def setup_actions(self):
        self.set_light_HSL = ActionHolder(
            plugin_base=self,
            action_base=SetLightAction,
            action_id="dev_uf_IkeaDirigera::SetLightHSL",
            action_name=self.lm.get("action.set-light-hsl.name"),
        )
        self.add_action_holder(self.set_light_HSL)

        self.set_light_RGB = ActionHolder(
            plugin_base=self,
            action_base=SetLightRGBAction,
            action_id="dev_uf_IkeaDirigera::SetLightRGB",
            action_name=self.lm.get("action.set-light-rgb.name"),
        )
        self.add_action_holder(self.set_light_RGB)

        self.effect_thunder = ActionHolder(
            plugin_base=self,
            action_base=EffectThunderAction,
            action_id="dev_uf_IkeaDirigera::EffectThunder",
            action_name=self.lm.get("action.effect-thunder"),
        )
        self.add_action_holder(self.set_light_RGB)

    def setup_backend(self):
        # Launch backend
        backend_path = Path(__file__).parent / "actions" / "backend.py"
        venv_path = Path(__file__).parent / ".venv"

        self.launch_backend(
            backend_path=backend_path, open_in_terminal=False, venv_path=venv_path
        )
        self.wait_for_backend(tries=5)
