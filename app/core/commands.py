from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

from app.core.config import config
from app.core.exceptions import ConfigError
from app.utils.config import YamlSettings

SYSTEM_COMMANDS = {"start", "ask", "goto", "state", "settings", "error"}


class Commands(YamlSettings):
    commands: dict[str, str] = {}

    @field_validator("commands", mode="before")
    def validate_commands(cls, commands):
        inter = SYSTEM_COMMANDS & set(commands.keys())
        if "start" in inter:
            raise ConfigError(
                "The start command must be specified in the 'messages.*.yml' file"
            )
        if len(inter) > 0:
            commands_str = ", ".join([f"'{command}'" for command in commands])
            raise ConfigError(f"{commands_str} cannot be changed")

        return commands

    model_config = SettingsConfigDict(yaml_file=config.paths.commands, frozen=True)


commands: Commands = Commands()


status = "Failed to check the status of commands"
if not config.paths.commands.exists():
    status = f"No commands loaded: File {str(config.paths.commands)} does not exists."
elif len(commands.model_fields_set) == 0:
    status = f"No commands loaded: File {str(config.paths.commands)} is empty."
else:
    status = f"Commands has been loaded from {str(config.paths.commands)}"
