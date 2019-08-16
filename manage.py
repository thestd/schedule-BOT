import sys
import os

if __name__ == '__main__':
    cmd = sys.argv[1]

    if cmd == 'run':
        from app.main import run

        try:
            token = os.environ["TOKEN"]
        except KeyError:
            raise RuntimeError("Please provide bot token")

        skip_updates = os.environ.get("SKIP_UPDATES", True)
        run(token, skip_updates)
