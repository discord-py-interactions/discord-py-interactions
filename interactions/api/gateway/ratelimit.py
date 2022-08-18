import asyncio
import logging
from sys import version_info
from time import time
from typing import Optional

log = logging.getLogger("gateway.ratelimit")


class WSRateLimit:
    """
    A class that controls Gateway ratelimits using locking and a timer.

    .. note ::
        While the docs state that the Gateway ratelimits are 120/60 (120 requests per 60 seconds),
        this ratelimit offsets to 115 instead of 120 for room.

    :ivar Lock lock: The gateway Lock object.
    :ivar int max: The upper limit of the ratelimit. Defaults to `115` seconds.
    :ivar int remaining: How many requests are left per ``per_second``. This is automatically decremented and reset.
    :ivar float current_limit: When this cooldown session began. This is defined automatically.
    :ivar float per_second: A constant denoting how many requests can be done per unit of seconds. (i.e., per 60 seconds, per 45, etc.)
    """

    def __init__(self, loop=Optional[asyncio.AbstractEventLoop]):
        self.lock = asyncio.Lock(loop=loop) if version_info < (3, 10) else asyncio.Lock()
        # To conserve timings, we need to do 115/60

        self.max = self.remaining = 115
        self.per_second = 60.0
        self.current_limit = 0.0

    def is_ratelimited(self):
        current = time()
        if current > self.current_limit + self.per_second:
            return False
        return self.remaining == 0

    def get_delay(self):
        current = time()

        if current > self.current_limit + self.per_second:
            self.remaining = self.max

        if self.remaining == self.max:
            self.current_limit = current

        if self.remaining == 0:
            return self.per_second - (current - self.current_limit)

        self.remaining -= 1
        if self.remaining == 0:
            self.current_limit = current

        return 0.0

    async def block(self):
        async with self.lock:
            if delta := self.get_delay():
                log.warning(f"We are ratelimited. Please wait {delta} seconds...")
                await asyncio.sleep(delta)
