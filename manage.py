import sys

if __name__ == '__main__':
    cmd = sys.argv[1]

    if cmd == 'run':
        from app.main import run
        run()
