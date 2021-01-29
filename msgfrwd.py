# By @xditya 
# https://github.com/xditya
# https://t.me/xditya

import logging
import asyncio
from telethon import TelegramClient, events
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# start the bot
apiid = config("APP_ID")
apihash = config("API_HASH")
bottoken = config("BOT_TOKEN")
msgfrwd = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)

@msgfrwd.on(events.NewMessage(pattern="/start"))
async def _(event):
    ok = await msgfrwd(GetFullUserRequest(event.sender_id))
    await event.reply(f"Hi {ok.user.first_name}, I am a message forwarder bot.\nRead /help for more!\n\n(c) @its_xditya")

@msgfrwd.on(events.NewMessage(pattern="/help"))
async def _(event):
    await event.reply("I forward messages from one group to another.\nAdd me to both the groups first...\nUse `/frwd <to group id/username> <message/reply to message>` to forward the message to that group.\n\n(c) @its_xditya")

@msgfrwd.on(events.NewMessage(pattern="/frwd"))
async def frwder(event):
    if event.is_private:
        await event.reply("I work in groups!")
        return
    ok = await msgfrwd(GetFullUserRequest(event.sender_id))
    txt = event.text.split(" ", maxsplit=2)
    try:
        chat = txt[1]
        msg = txt[2]
        if msg is None:
            await event.reply("No message provided!\n\nFormat - `/frwd <chat id/username> <message/reply to message>`")
            return
        if chat.startswith('@'):
            try:
                temp = await msgfrwd.get_entity(chat)
                chat = temp.id
            except UsernameNotOccupiedError as e:
                await event.reply(str(e))
                return
        try:
            sent = await msgfrwd.send_message(chat, msg)
            await sent.reply(f"Message from [{ok.user.first_name}](tg://user?id={event.sender_id})")
            temp = await event.reply("Done!")
            await asyncio.sleep(10)
            #await event.delete()
            await temp.delete()
        except Exception as e:
            await event.reply(f"Bot not in the group 🤔\n\n{str(e)}")
    except UsernameNotOccupiedError as e:
        await event.reply(str(e))
        return
    except Exception as e:
        await event.reply(f"Format - `/frwd <chat id/username> <message/reply to message>`\n\n{str(e)}")
        return

print("Bot has started.")
msgfrwd.run_until_disconnected()
