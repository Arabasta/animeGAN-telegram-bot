from telegram import Update
from src.Config import Config
from src.state.UserModel import UserModelManager
import os

from src.util.Logger import LoggerFactory


class MessageHandlers:
    def __init__(self, bot, converter, user_model_manager: UserModelManager):
        self.log = LoggerFactory.get_logger(self.__class__.__name__)
        self.bot = bot
        self.converter = converter
        self.user_model_manager = user_model_manager

    async def handle_photo(self, update: Update):
        chat_id = update.message.chat.id
        try:
            self.log.info(f"Processing image for chat {chat_id}")
            await self.bot.send_message(chat_id, "Processing image...")

            photo = update.message.photo[-1]  # max resolution
            model = self.user_model_manager.get_model(chat_id, update.message.caption)

            file = await self.bot.get_file(photo.file_id)
            output_path = await self.converter.process_image(file, model)

            # send result
            with open(output_path, "rb") as photo_file:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,
                    caption=f"Converted using {model} model")
        except Exception as e:
            await self.bot.send_message(chat_id, f"Error processing image: {str(e)}")
            self.log.error(f"Image processing failed for {chat_id}: {str(e)}", exc_info=True)

        finally:
            if 'output_path' in locals() and os.path.exists(output_path):
                os.unlink(output_path)

    async def handle_text(self, update: Update):
        text = update.message.text.lower().strip()
        chat_id = update.message.chat.id

        if text == '/hayao' or text == 'ghibli':
            await self._switch_model(chat_id, "hayao")
        elif text == '/shinkai' or text == 'yourname':
            await self._switch_model(chat_id, "shinkai")
        elif text == '/current' or text == '/default':
            await self._show_current_model(chat_id)
        elif text == '/help':
            await self._send_help(chat_id)
        elif text == '/start':
            await self.bot.send_message(chat_id, "Welcome! Send me a photo to convert to anime style.")
        else:
            await self.default_message(chat_id)

    async def _switch_model(self, chat_id: int, model: str):
        if Config.IS_STATELESS:
            await self.bot.send_message(
                chat_id,
                "Model switching disabled in stateless mode\n"
                "Include model in photo caption:\n"
                "Example: '/shinkai' as caption")
            return

        if self.user_model_manager.set_model(chat_id, model):
            await self.bot.send_message(chat_id, f"Switched to {model} model")
        else:
            await self.bot.send_message(chat_id, "Invalid model specified")

    async def _show_current_model(self, chat_id: int):
        model = self.user_model_manager.get_model(chat_id)
        await self.bot.send_message(chat_id, f"Current model: {model}")

    async def _send_help(self, chat_id: int):
        if Config.IS_STATELESS:
            message = (
                "Send me a photo to convert to anime style.\n\n"
                "Image Caption Commands:\n"
                "    /hayao - Use Hayao model (default)\n"
                "    /shinkai - Use Shinkai model\n"
                "Text Commands:\n"
                "    /default - Show default model\n"
                "    /help - Show this message")
        else:
            message = (
                "Send me a photo to convert to anime style.\n\n"
                "Commands:\n"
                "    /hayao - Use Hayao model\n"
                "    /shinkai - Use Shinkai model\n"
                "    /current - Show current model\n"
                "    /help - Show this message")

        await self.bot.send_message(chat_id, message)

    async def default_message(self, chat_id: int):
        await self.bot.send_message(
            chat_id,
            "Please send a photo or use /help"
        )
