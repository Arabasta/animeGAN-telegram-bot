import asyncio
import telegram
from src.Config import Config
from src.bot.MessageHandlers import MessageHandlers
from src.state.UserModel import UserModelManager
from src.model.AnimeGANConverter import AnimeGANConverter


class AnimeBot:
    def __init__(self):
        self.bot = telegram.Bot(Config.TELEGRAM_TOKEN)
        self.converter = AnimeGANConverter(Config.MODEL_PATHS)
        self.state_manager = UserModelManager()
        self.handlers = MessageHandlers(self.bot, self.converter, self.state_manager)
        self.semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT_REQUESTS)

    async def handle_updates(self):
        offset = None
        while True:
            updates = await self.bot.get_updates(offset=offset, timeout=10)
            for update in updates:
                offset = update.update_id + 1
                if update.message:
                    async with self.semaphore:
                        await self._dispatch_update(update)

    async def _dispatch_update(self, update):
        if update.message.photo:
            await self.handlers.handle_photo(update)
        elif update.message.text:
            await self.handlers.handle_text(update)
        else:
            await self.handlers.default_message(update.message.chat.id)