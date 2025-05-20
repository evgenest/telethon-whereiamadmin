import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import ChatAdminRequiredError
from dotenv import load_dotenv

load_dotenv()  # подгружает переменные из .env в os.environ

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
            print(f"{dialog.title} — вы админ")
    
    # Выводим итоговый список
    if admin_dialogs:
        print("\n=== Итоговый список ===")
        for index, (title, chat_type, link) in enumerate(admin_dialogs, start=1):
            print(f"{index}. {title} ({chat_type}) — {link}")
    else:
        print("\nВы не найдены как администратор ни в одном чате.")

if __name__ == '__main__':
    # Считываем переменные окружения; API_ID приходит как строка — приводим к int
    api_id = int(os.environ['API_ID'])
    api_hash = os.environ['API_HASH']
    
    # Если есть сохранённая строковая сессия, используем её. Иначе – файловая сессия.
    session_str = os.environ.get('TELEGRAM_SESSION_BASE64', '')
    if session_str:
        client = TelegramClient(StringSession(session_str), api_id, api_hash)
    else:
        client = TelegramClient('session_name', api_id, api_hash)
    
    # Запускаем авторизацию. Если сессия новая, авторизация пройдёт интерактивно.
    client.start()
    
    client.loop.run_until_complete(main())