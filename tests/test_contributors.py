from mock import MagicMock, patch
from nose.tools import eq_, raises

import gease.exceptions as exceptions
from gease.contributors import EndPoint


class TestPublish:
    @patch("gease.contributors.Api.get_api")
    def test_all_contributors(self, fake_api):
        sample_reply = [
            {
                "login": "howdy",
                "id": 4280312,
                "node_id": "MDQ6VXNlcjQyODAzMTI=",
                "avatar_url": "https://avatars0.githubusercontent.com/u/4280312?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/howdy",
                "html_url": "https://github.com/howdy",
                "followers_url": "https://api.github.com/users/howdy/followers",
                "following_url": "https://api.github.com/users/howdy/following{/other_user}",
                "gists_url": "https://api.github.com/users/howdy/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/howdy/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/howdy/subscriptions",
                "organizations_url": "https://api.github.com/users/howdy/orgs",
                "repos_url": "https://api.github.com/users/howdy/repos",
                "events_url": "https://api.github.com/users/howdy/events{/privacy}",
                "received_events_url": "https://api.github.com/users/howdy/received_events",
                "type": "User",
                "site_admin": False,
                "contributions": 259,
            }
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(side_effect=[sample_reply, {"name": "hello world"}])
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        eq_(
            contributors,
            [
                {
                    "name": "hello world",
                    "url": "https://api.github.com/users/howdy",
                }
            ],
        )
