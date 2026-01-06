import asyncio

import aiohttp

from abc import ABC, abstractmethod


class HttpClient:
    def __init___(self):
        self.conn = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=450
        )

        self.timeout_session = aiohttp.ClientTimeout(
            total=30,
            connect=20
        )

        self.session = aiohttp.ClientSession(connector=self.conn, timeout=self.timeout_session)