from aiogram import Bot, types
from aiogram.utils.exceptions import MessageToDeleteNotFound, \
    MessageCantBeDeleted

import app.core.misc as misc


class ClearBot(Bot):
    async def send_message(self, chat_id, *args,
                           **kwargs) -> types.Message:
        res = await super(ClearBot, self).send_message(chat_id, *args,
                                                       **kwargs)
        usr_data = await misc.storage.get_data(
            chat=chat_id,
            user=chat_id
        )
        if "msg_to_delete" not in usr_data or not usr_data["msg_to_delete"]:
            await misc.storage.update_data(
                chat=chat_id,
                user=chat_id,
                data={"msg_to_delete": [res.message_id]}
            )
            return res

        for msg in usr_data["msg_to_delete"]:
            await self.delete_message(
                chat_id,
                msg
            )

        await misc.storage.update_data(
            chat=chat_id,
            user=chat_id,
            data={"msg_to_delete": [res.message_id]}
        )
        return res
