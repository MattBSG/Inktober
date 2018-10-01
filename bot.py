import discord
import logging
import backend.logging
import backend.config
import datetime
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    def reload_extension(self, name: str):
        self.unload_extension(name)
        self.load_extension(name)

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)


inktober = Bot(command_prefix="b!")


@inktober.event
async def on_ready():
    log.info(f"Connected at {datetime.datetime.now().strftime('%d %H:%M:%S')}")
    log.info(f"Logged in as {inktober.user.name} {inktober.user.id}")
    log.info("Connected to: ")

    for server in inktober.servers:
        log.info(server)

    await inktober.change_presence(game=discord.Game(name="Haunting blobkind"), status=None, afk=False)


if __name__ == "__main__":
    with backend.logging.setup_logging():
        log = logging.getLogger(__name__)

        try:
            inktober.load_extension("backend.module_loader")
        except Exception as E:
            exc = "{}: {}".format(type(E).__name__, E)
            log.error("Failed to load extension {}\n{}".format("backend.module_loader", exc))

    inktober.run(backend.config.discord_token)
