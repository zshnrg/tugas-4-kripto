import asyncio
import requests

class Supabase():
    def __init__(self, public_key: str, url: str):
        self.public_key = public_key
        self.url = url

    def getUser(self, email: str):
        asyncio.create_task(self._getUser(email))

    async def _getUser(self, email: str):
        data = await requests.get(
            f"{self.url}/rest/v1/users?apikey={email}",
            headers={
                "apikey": self.public_key
            }
        )