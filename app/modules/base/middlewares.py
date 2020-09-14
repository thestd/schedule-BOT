import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.core.amplitude import AmplitudeEvent, UPDATE_MESSAGE_EVENT, amplitude_log, UPDATE_CALLBACK_EVENT, \
    UserProperties


class StatisticMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            logging.info(
                f"New update: {update.message}"
            )
        elif update.callback_query:
            logging.info(
                f"New update: {update.callback_query}"
            )


class AmplitudeMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user
            event = AmplitudeEvent(
                event_type=UPDATE_MESSAGE_EVENT,
                user_id=str(user.id),
                user_properties=UserProperties.from_telegram_user(user)
            )
            try:
                await amplitude_log(event)
            except Exception:
                logging.exception("Error while sending amplitude log.")
        elif update.callback_query:
            user = update.callback_query.from_user
            event = AmplitudeEvent(
                event_type=UPDATE_CALLBACK_EVENT,
                user_id=str(user.id),
                user_properties=UserProperties.from_telegram_user(user)
            )
            try:
                await amplitude_log(event)
            except Exception:
                logging.exception("Error while sending amplitude log.")
