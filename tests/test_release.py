from nose.tools import raises
from gease.release import EndPoint
from mock import patch, MagicMock
import gease.exceptions as exceptions


class TestRelease:

    def setUp(self):
        self.patcher = patch('gease.release.Api')
        self.fake_api_singleton = self.patcher.start()
        self.fake_api = MagicMock()
        self.fake_api_singleton.get_api = self.fake_api
        self.patcher2 = patch('gease.rest.get_token')
        self.fake_token = self.patcher2.start()
        self.fake_token.return_value = 'token'

    def tearDown(self):
        self.patcher2.stop()
        self.patcher.stop()

    def test_create_release(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                return_value={'html_url': 'aurl'}
            )
        )
        release = EndPoint('owner', 'repo')
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_unknown_error(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                return_value={}
                )
            )
        release = EndPoint('owner', 'repo')
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_release_exist(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.ReleaseExistException
                )
            )
        release = EndPoint('owner', 'repo')
        release.publish(hello='world', tag_name='existing tag')

    @raises(exceptions.AbnormalGithubResponse)
    def test_repo_not_found(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.RepoNotFoundError
                )
            )
        release = EndPoint('owner', 'repo')
        release.republish = MagicMock(
            side_effect=exceptions.RepoNotFoundError)
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_unhandled_exception(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.UnhandledException
                )
            )
        release = EndPoint('owner', 'repo')
        release.publish(hello='world')
