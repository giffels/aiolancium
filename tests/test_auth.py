from aiolancium.auth import Authenticator

from .utilities.utilities import run_async

from unittest import TestCase

from aioresponses import aioresponses
from aioresponses.compat import URL
from aioresponses.core import RequestCall
from aiohttp.client_exceptions import ClientResponseError


class TestAuthenticator(TestCase):
    def setUp(self) -> None:
        self.auth = Authenticator(api_key="test123")

    def test_get_token(self):
        with aioresponses() as m:
            m.post(
                "https://portal.lancium.com/api/v1/access_tokens",
                headers={"Authorization": "test_granted"},
            )
            self.assertEqual(run_async(self.auth.get_token), "test_granted")

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
        self.assertFalse(self.auth.is_token_valid)

        with aioresponses() as m:
            m.post(
                "https://portal.lancium.com/api/v1/access_tokens",
                headers={"Authorization": "test_granted"},
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
