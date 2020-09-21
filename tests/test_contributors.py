from mock import MagicMock, patch
from nose.tools import eq_

from gease.contributors import EndPoint


class TestPublish:
    @patch("gease.contributors.Api.get_public_api")
    def test_all_contributors(self, fake_api):
        sample_reply = [
            {"login": "howdy", "url": "https://api.github.com/users/howdy"}
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(
                side_effect=[
                    sample_reply,
                    {"name": "hello world", "html_url": ""},
                ]
            )
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        eq_(
            contributors,
            [{"name": "hello world", "html_url": ""}],
        )

    @patch("gease.contributors.Api.get_public_api")
    def test_no_names(self, fake_api):
        sample_reply = [
            {"login": "howdy", "url": "https://api.github.com/users/howdy"}
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(
                side_effect=[sample_reply, {"name": None, "html_url": ""}]
            )
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        eq_(
            contributors,
            [{"name": "howdy", "html_url": ""}],
        )
