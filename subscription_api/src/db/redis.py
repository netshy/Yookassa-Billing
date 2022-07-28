class RedisStorage:
    def __init__(self, cache_engine):
        self.cache_engine = cache_engine

    async def get(self, key: str):
        return await self.cache_engine.get(key)

    async def set(self, key: str, value: str, expire: int):
        return await self.cache_engine.set(key, value, expire=expire)

    async def close_connection(self):
        await self.cache_engine.close()
