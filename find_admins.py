from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins

api_id = 123456         # ваш API ID
api_hash = 'your_hash'  # ваш API Hash

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            # получаем список админов диалога
            admins = await client.get_participants(dialog, filter=ChannelParticipantsAdmins)
            # проверяем, есть ли среди них наш пользователь
            if any(a.id == (await client.get_me()).id for a in admins):
                print(f"{dialog.title} — вы админ")

with client:
    client.loop.run_until_complete(main())
