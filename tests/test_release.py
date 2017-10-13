from nose.tools import raises
from gease.release import EndPoint
from mock import patch, MagicMock
import gease.exceptions as exceptions


class TestRelease:

    def setUp(self):
        self.patcher = patch('gease.release.Api')
        self.fake_api = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_create_release(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                return_value={'html_url': 'aurl'}
            )
        )
        release = EndPoint('token', 'owner', 'repo')
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_unknown_error(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                return_value={}
                )
            )
        release = EndPoint('token', 'owner', 'repo')
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_release_exist(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.ReleaseExistException
                )
            )
        release = EndPoint('token', 'owner', 'repo')
        release.publish(hello='world', tag_name='existing tag')

    @raises(exceptions.AbnormalGithubResponse)
    def test_repo_not_found(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.RepoNotFoundError
                )
            )
        release = EndPoint('token', 'owner', 'repo')
        release.publish(hello='world')

    @raises(exceptions.AbnormalGithubResponse)
    def test_unhandled_exception(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(
                side_effect=exceptions.UnhandledException
                )
            )
        release = EndPoint('token', 'owner', 'repo')
        release.publish(hello='world')
