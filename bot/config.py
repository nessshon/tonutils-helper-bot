from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    BOT_TOKEN: str


def load_config() -> Config:
    """ Load config from environment variables. """
    env = Env()
    env.read_env()

    return Config(
        BOT_TOKEN=env.str("BOT_TOKEN"),
    )
