import os
import sys
import mock
from gease.main import get_token, main, DEFAULT_RELEASE_MESSAGE
import gease.exceptions as exceptions
from nose.tools import eq_, raises

TEST_TAG = 'tag'
SHORT_ARGS = ['gs', 'repo', TEST_TAG]


class TestMain:

    def setUp(self):
        self.patcher = mock.patch('gease.main.os.path.expanduser')
        self.fake_expand = self.patcher.start()
        self.fake_expand.return_value = os.path.join('tests', 'fixtures')

        self.patcher2 = mock.patch('gease.main.EndPoint')
        self.fake_release = self.patcher2.start()

    def tearDown(self):
        self.patcher2.stop()
        self.patcher.stop()

    def test_get_token(self):
        user, token = get_token()
        eq_(user, 'test')
        eq_(token, 'test')

    @raises(exceptions.NoGeaseConfigFound)
    def test_no_gease_file(self):
        self.fake_expand.return_value = os.path.join('tests')
        user, token = get_token()

    def test_good_commands(self):
        create_method = mock.MagicMock(
            return_value='http://localhost/tag/testurl')
        self.fake_release.return_value = mock.MagicMock(publish=create_method)
        with mock.patch.object(sys, 'argv', SHORT_ARGS):
            main()
            create_method.assert_called_with(
                tag_name=TEST_TAG,
                name=TEST_TAG,
                body=DEFAULT_RELEASE_MESSAGE)

    def test_custom_release_message(self):
        release_message = ['hello', 'world', 'you', 'see', 'it']
        create_method = mock.MagicMock(
            return_value='http://localhost/tag/testurl')
        self.fake_release.return_value = mock.MagicMock(publish=create_method)
        with mock.patch.object(sys, 'argv', SHORT_ARGS + release_message):
            main()
            create_method.assert_called_with(
                tag_name=TEST_TAG,
                name=TEST_TAG,
                body=' '.join(release_message))

    def test_quoted_release_message(self):
        release_message = 'hello world you see it'
        create_method = mock.MagicMock(
            return_value='http://localhost/tag/testurl')
        self.fake_release.return_value = mock.MagicMock(publish=create_method)
        with mock.patch.object(sys, 'argv', SHORT_ARGS + [release_message]):
            main()
            create_method.assert_called_with(
                tag_name=TEST_TAG,
                name=TEST_TAG,
                body=release_message)

    def test_existing_release(self):
        create_method = mock.MagicMock(
            side_effect=exceptions.ReleaseExistException)
        self.fake_release.return_value = mock.MagicMock(publish=create_method)
        with mock.patch.object(sys, 'argv', SHORT_ARGS):
            main()
            create_method.assert_called_with(
                tag_name=TEST_TAG,
                name=TEST_TAG,
                body=DEFAULT_RELEASE_MESSAGE)

    def test_unknown_protocol_change(self):
        create_method = mock.MagicMock(
            side_effect=exceptions.UnhandledException)
        self.fake_release.return_value = mock.MagicMock(publish=create_method)
        with mock.patch.object(sys, 'argv', SHORT_ARGS):
            main()
            create_method.assert_called_with(
                tag_name=TEST_TAG,
                name=TEST_TAG,
                body=DEFAULT_RELEASE_MESSAGE)


@raises(SystemExit)
def test_no_args():
    with mock.patch.object(sys, 'argv', []):
        main()


@raises(SystemExit)
def test_insufficent_args():
    with mock.patch.object(sys, 'argv', SHORT_ARGS[:2]):
        main()
