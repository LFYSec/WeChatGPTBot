from typing import Optional, Union
import asyncio
from chat import *
from wechaty_puppet import get_logger
from wechaty import (
    Wechaty,
    Contact,
    Room,
    Message,
    EventReadyPayload
)

token = ""
logger = get_logger(__name__)

class MyBot(Wechaty):
    def __init__(self) -> None:
        self.login_user: Optional[Contact] = None
        super().__init__()

    async def on_ready(self, payload: EventReadyPayload) -> None:
        logger.info('ready event %s...', payload)

    async def on_login(self, contact: Contact) -> None:
        logger.info('Contact<%s> has logined ...', contact)
        self.login_user = contact

    async def on_message(self, msg: Message) -> None:
        from_contact: Contact = msg.talker()
        text: str = msg.text()
        room: Optional[Room] = msg.room()
        conv: Union[Room, Contact] = from_contact if room is None else room
        await conv.ready()

        if "chat:" in text:
            text = text.replace("chat:\n", "").replace("chat:", "")
            if msg.room():
                logger.info(f"[*]Group Message: {text}")
                contact_id = msg.talker().contact_id
                chat_res = await chatgpt(text, token)
                await conv.say(chat_res, mention_ids=[contact_id])
            else:
                logger.info(f"[*]Personal Message: {text}")
                chat_res = await chatgpt(text, token)
                await conv.say(chat_res)


async def main():
    bot = MyBot()
    await bot.start()

if __name__ == "__main__":
    try:
        token = get_chat_token()
        logger.info(token)
    except Exception as e:
        logger.error(e)
                        
    asyncio.run(main())