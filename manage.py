import os

import sentry_sdk
import sys

from sentry_sdk.integrations.aiohttp import AioHttpIntegration

if __name__ == '__main__':
    cmd = sys.argv[1]

    if cmd == 'run':
        SENTRY_HOST = os.getenv("SENTRY_HOST")
        if SENTRY_HOST:
            sentry_sdk.init(
                SENTRY_HOST,
                integrations=[AioHttpIntegration()]
            )
        from app.main import run
        run()
