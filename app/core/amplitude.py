import logging
from dataclasses import dataclass, asdict
from typing import Optional

import aiohttp

from app.core.config import AMPLITUDE_URL, AMPLITUDE_API_KEY

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*'
}

UPDATE_MESSAGE_EVENT = "update_message_event"
UPDATE_CALLBACK_EVENT = "update_callback_event"


@dataclass
class UserProperties:
    username: Optional[str]
    user_first_name: Optional[str]
    user_last_name: Optional[str]

    @classmethod
    def from_telegram_user(cls, user):
        return cls(
            username=user.username,
            user_first_name=user.first_name,
            user_last_name=user.last_name
        )


@dataclass
class AmplitudeEvent:
    user_id: str
    event_type: str
    user_properties: UserProperties


async def amplitude_log(event: AmplitudeEvent) -> None:
    post_data = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [asdict(event)]
    }
    logging.debug(post_data)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(AMPLITUDE_URL, json=post_data) as resp:
            msg = f"Response from amplitude: {await resp.json()}"
            logging.debug(msg)
