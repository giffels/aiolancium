from aiolancium.auth import Authenticator

from .utilities.utilities import run_async

from time import time
from unittest import TestCase

from aioresponses import aioresponses
from aioresponses.compat import URL
from aioresponses.core import RequestCall
from aiohttp.client_exceptions import ClientResponseError

import jwt


class TestAuthenticator(TestCase):
    def setUp(self) -> None:
        self.auth = Authenticator(api_key="test123")

    def test_get_token(self):
        test_token = f"Bearer {jwt.encode(dict(exp=int(time())), key='Test')}"

        with aioresponses() as m:
            m.post(
                "https://portal.lancium.com/api/v1/access_tokens",
                headers={"Authorization": test_token},
            )
            self.assertEqual(run_async(self.auth.get_token), test_token)

            self.assertDictEqual(  # check assert called with
                m.requests,
                {
                    ("POST", URL("https://portal.lancium.com/api/v1/access_tokens")): [
                        RequestCall(
                            args=(),
                            kwargs={
                                "data": None,
                                "headers": {"Authorization": "Bearer test123"},
                            },
                        )
                    ]
                },
            )

    def test_get_token_404(self):
        with aioresponses() as m:
            m.post("https://portal.lancium.com/api/v1/access_tokens", status=404)
            with self.assertRaises(ClientResponseError) as se:
                run_async(self.auth.get_token)
            self.assertTrue("404" in str(se.exception))

    def test_is_token_valid(self):
        test_token = f"Bearer {jwt.encode(dict(exp=int(time() + 120)), key='Test')}"
        self.assertFalse(self.auth.is_token_valid)

        with aioresponses() as m:
            m.post(
                "https://portal.lancium.com/api/v1/access_tokens",
                headers={"Authorization": test_token},
            )
            run_async(self.auth.get_token)

            self.assertTrue(self.auth.is_token_valid)

            run_async(self.auth.get_token)

            self.assertEqual(
                len(
                    m.requests[
                        ("POST", URL("https://portal.lancium.com/api/v1/access_tokens"))
                    ]
                ),
                1,
            )  # check call count
