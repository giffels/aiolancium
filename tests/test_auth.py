from aiolancium.auth import Authenticator

from .utilities.utilities import run_async
from .utilities.utilities import set_awaitable_return_value

from unittest import TestCase
from unittest.mock import patch

import httpx


class TestAuthenticator(TestCase):
    def setUp(self) -> None:
        self.auth = Authenticator(api_key="test123")

    @patch("httpx.AsyncClient.post")
    def test_get_token(self, mock_post):
        set_awaitable_return_value(
            mock_post,
            httpx.Response(
                200,
                request=httpx.Request(method="fake", url="fake"),
                headers={"Authorization": "test_granted"},
            ),
        )
        run_async(self.auth.get_token)
        mock_post.assert_called_with(
            headers={"Authorization": "Bearer test123"},
            url="https://portal.lancium.com/api/v1/access_tokens",
        )

    @patch("httpx.AsyncClient.post")
    def test_get_token_404(self, mock_post):
        set_awaitable_return_value(
            mock_post,
            httpx.Response(
                404,
                request=httpx.Request(method="fake", url="fake"),
            ),
        )
        with self.assertRaises(httpx.HTTPStatusError) as se:
            run_async(self.auth.get_token)
        self.assertTrue("404" in str(se.exception))

    @patch("httpx.AsyncClient.post")
    def test_is_token_valid(self, mock_post):
        self.assertFalse(self.auth.is_token_valid)

        set_awaitable_return_value(
            mock_post,
            httpx.Response(
                200,
                request=httpx.Request(method="fake", url="fake"),
                headers={"Authorization": "test_granted"},
            ),
        )
        run_async(self.auth.get_token)

        self.assertTrue(self.auth.is_token_valid)

        run_async(self.auth.get_token)
        self.assertEqual(mock_post.call_count, 1)
