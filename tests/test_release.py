from nose.tools import raises
from gease.release import EndPoint
from mock import patch, MagicMock
import gease.exceptions as exceptions


@patch('gease.release.Api')
def test_create_release(fake_api):
    fake_api.return_value = MagicMock(
        create=MagicMock(
            return_value={'html_url': 'aurl'}
            )
        )
    release = EndPoint('token', 'owner', 'repo')
    release.publish(hello='world')


@raises(exceptions.AbnormalGithubResponse)
@patch('gease.release.Api')
def test_unknown_error(fake_api):
    fake_api.return_value = MagicMock(
        create=MagicMock(
            return_value={}
            )
        )
    release = EndPoint('token', 'owner', 'repo')
    release.publish(hello='world')
