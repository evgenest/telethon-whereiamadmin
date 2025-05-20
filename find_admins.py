import os
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import ChatAdminRequiredError

async def main():
    my_info = await client.get_me()
    my_id = my_info.id
    admin_dialogs = []
    
    async for dialog in client.iter_dialogs():
        if not (dialog.is_group or dialog.is_channel):
            continue

        try:
            admins = await client.get_participants(dialog, filter=ChannelParticipantsAdmins)
        except ChatAdminRequiredError:
            # Если нет доступа для получения списка админов, пропускаем чат
            continue

        if any(admin.id == my_id for admin in admins):
            # Определяем тип чата для вывода
            chat_type = "group" if dialog.is_group else "channel" if dialog.is_channel else "чат"
            
            # Пытаемся сформировать ссылку. Если поле username доступно, собираем https://t.me/username.
            try:
                if getattr(dialog.entity, 'username', None):
                    link = f"https://t.me/{dialog.entity.username}"
                else:
                    link = "Нет публичной ссылки"
            except Exception:
                link = "Не удалось получить ссылку"
            
            admin_dialogs.append((dialog.title, chat_type, link))
            # Выводим промежуточное сообщение
            print(f"{dialog.title} — вы админ")
    
    # Выводим итоговый список
    if admin_dialogs:
        print("\n=== Итоговый список ===")
        for index, (title, chat_type, link) in enumerate(admin_dialogs, start=1):
            print(f"{index}. {title} ({chat_type}) — {link}")
    else:
        print("\nВы не найдены как администратор ни в одном чате.")

if __name__ == '__main__':
    # Считываем переменные окружения; API_ID приходит как строка – приводим к int
    api_id = int(os.environ['API_ID'])
    api_hash = os.environ['API_HASH']
    bot_token = os.environ.get('BOT_TOKEN')
    
    client = TelegramClient('session_name', api_id, api_hash)
    
    # Если задан BOT_TOKEN, используем его для автоматической авторизации без ввода
    if bot_token:
        client.start(bot_token=bot_token)
    else:
        client.start()
    
    client.loop.run_until_complete(main())