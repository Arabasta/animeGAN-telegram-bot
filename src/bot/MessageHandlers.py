from telegram import Update
from src.state.State import UserStateManager
import os


class MessageHandlers:
    def __init__(self, bot, converter, state_manager: UserStateManager):
        self.bot = bot
        self.converter = converter
        self.state_manager = state_manager

    async def handle_photo(self, update: Update):
        chat_id = update.message.chat.id
        await self.bot.send_message(chat_id, "Received your image! Processing...")

        photo = update.message.photo[-1]
        file = await self.bot.get_file(photo.file_id)

        model_type = self.state_manager.get_user_state(chat_id).current_model
        output_path = await self.converter.process_image(file, model_type)

        with open(output_path, "rb") as photo_file:
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=photo_file,
                caption=f"Converted using {model_type} model"
            )

        os.unlink(output_path)

    async def handle_text(self, update: Update):
        text = update.message.text.lower()
        chat_id = update.message.chat.id

        if text == '/start':
            await self._send_welcome(chat_id)
        elif text == '/hayao':
            await self._switch_model(chat_id, "hayao")
        elif text == '/shinkai':
            await self._switch_model(chat_id, "shinkai")
        elif text == '/current':
            await self._show_current_model(chat_id)
        else:
            await self.bot.send_message(chat_id, "Please send a photo or use /help")

    async def _send_welcome(self, chat_id: int):
        message = (
            "Welcome to AnimeGAN Bot!\n"
            "Send me a photo to convert to anime style.\n"
            "Commands:\n"
            "/hayao - Use Hayao model (default)\n"
            "/shinkai - Use Shinkai model\n"
            "/current - Show current model"
        )
        await self.bot.send_message(chat_id, message)

    async def _switch_model(self, chat_id: int, model: str):
        self.state_manager.set_model(chat_id, model)
        await self.bot.send_message(chat_id, f"Switched to {model} model")

    async def _show_current_model(self, chat_id: int):
        model = self.state_manager.get_user_state(chat_id).current_model
        await self.bot.send_message(chat_id, f"Current model: {model}")