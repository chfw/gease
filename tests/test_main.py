import os
import sys
import mock
from gease.main import get_token, main, DEFAULT_RELEASE_MESSAGE
import gease.exceptions as exceptions
from nose.tools import eq_, raises


@mock.patch('gease.main.os.path.expanduser')
def test_get_token(fake_expand):
    fake_expand.return_value = os.path.join('tests', 'fixtures')
    user, token = get_token()
    eq_(user, 'test')
    eq_(token, 'test')


@raises(exceptions.NoGeaseConfigFound)
@mock.patch('gease.main.os.path.expanduser')
def test_no_gease_file(fake_expand):
    fake_expand.return_value = os.path.join('tests')
    user, token = get_token()


@mock.patch('gease.main.os.path.expanduser')
@mock.patch('gease.main.EndPoint')
def test_good_commands(fake_release, fake_expand):
    fake_expand.return_value = os.path.join('tests', 'fixtures')
    create_method = mock.MagicMock(return_value='http://localhost/tag/testurl')
    fake_release.return_value = mock.MagicMock(publish=create_method)
    args = ['gs', 'repo', 'tag']
    with mock.patch.object(sys, 'argv', args):
        main()
        create_method.assert_called_with(
            tag_name='tag',
            name='tag',
            body=DEFAULT_RELEASE_MESSAGE)


@mock.patch('gease.main.os.path.expanduser')
@mock.patch('gease.main.EndPoint')
def test_existing_release(fake_release, fake_expand):
    fake_expand.return_value = os.path.join('tests', 'fixtures')
    create_method = mock.MagicMock(
        side_effect=exceptions.ReleaseExistException)
    fake_release.return_value = mock.MagicMock(publish=create_method)
    args = ['gs', 'repo', 'tag']
    with mock.patch.object(sys, 'argv', args):
        main()
        create_method.assert_called_with(
            tag_name='tag',
            name='tag',
            body=DEFAULT_RELEASE_MESSAGE)
