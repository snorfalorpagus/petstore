#!/usr/bin/env python
import asyncio

from app import create_app

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main():
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
