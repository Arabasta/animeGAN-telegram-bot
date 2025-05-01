import asyncio
from src.bot.AnimeBot import AnimeBot


async def main():
    bot = AnimeBot()
    print("Bot is running...")
    await bot.handle_updates()

if __name__ == '__main__':
    asyncio.run(main())
