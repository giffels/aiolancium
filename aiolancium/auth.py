import aiohttp
import jwt
from time import time


class Authenticator(object):
    def __init__(self, api_key: str) -> None:
        self.data = {"Authorization": f"Bearer {api_key}"}
        self.token = None
        self.token_expires_on = 0
        self._url = "https://portal.lancium.com/api/v1/access_tokens"

    def get_expiry_date(self) -> int:
        decoded_token = jwt.decode(
            self.token.split()[1],  # token contains "Bearer <Token>"
            algorithms=["HS256"],
            options={"verify_signature": False, "verify_aud": False},
        )
        return decoded_token["exp"]

    async def get_token(
        self,
    ) -> str:  # Should be replaced by async properties once available
        if not (self.token and self.is_token_valid):
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.post(url=self._url, headers=self.data) as response:
                    self.token = response.headers.get("Authorization")
                    self.token_expires_on = self.get_expiry_date()
        return self.token

    @property
    def is_token_valid(self) -> float:
        return (
            self.token_expires_on - time() > 60
        )  # token should be at least valid for 60 s
