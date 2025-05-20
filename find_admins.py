import os
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins

# Считываем необходимые параметры из переменных окружения
api_id = int(os.environ['API_ID'])            # API_ID передаётся как строка, конвертируем в int
api_hash = os.environ['API_HASH']
bot_token = os.environ.get('BOT_TOKEN')         # BOT_TOKEN может быть не задан, поэтому используем get()

# Создаем клиента
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            # Получаем список админов диалога
            admins = await client.get_participants(dialog, filter=ChannelParticipantsAdmins)
            # Проверяем, является ли текущий пользователь администратором
            if any(a.id == (await client.get_me()).id for a in admins):
                print(f"{dialog.title} — вы админ")

if __name__ == '__main__':
    # Если BOT_TOKEN задан, запускаем клиента как бота (без интерактивного ввода)
    if bot_token:
        client.start(bot_token=bot_token)
    else:
        client.start()
    client.loop.run_until_complete(main())