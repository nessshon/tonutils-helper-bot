from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .router import router
from .config import load_config
from .logger import setup_logger


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """
    Shutdown event handler. This runs when the bot shuts down.

    :param dispatcher: Dispatcher: The bot dispatcher.
    :param bot: Bot: The bot instance.
    """
    await dispatcher.storage.close()
    await bot.delete_webhook()
    await bot.session.close()


async def on_startup(bot: Bot) -> None:
    """
    Startup event handler. This runs when the bot starts up.

    :param bot: Bot: The bot instance.
    """


async def main() -> None:
    config = load_config()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dp = Dispatcher(
        storage=MemoryStorage(),
        config=config,
        bot=bot,
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    import asyncio

    setup_logger()
    asyncio.run(main())
