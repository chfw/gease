from nose.tools import raises
from gease.rest import Api
from gease.exceptions import ReleaseExistException
from mock import patch, MagicMock


SAMPLE_422_ERROR = {
    'errors': [
        {'code': 'already_exists',
         'field': 'tag_name',
         'resource': 'Release'}
    ],
    'documentation_url': 'https://.../#create-a-release',
    'message': 'Validation Failed'
}


class TestApi:
    def setUp(self):
        self.patcher = patch('gease.rest.requests.Session')
        self.fake_session = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_create(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=201,
                    json=MagicMock(return_value={})
                )
            )
        )
        api = Api('test')
        api.create('http://localhost/', 'cool')

    @raises(ReleaseExistException)
    def test_existing_release(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=422,
                    json=MagicMock(return_value=SAMPLE_422_ERROR)
                )
            )
        )
        api = Api('test')
        api.create('http://localhost/', 'cool')

    @raises(Exception)
    def test_unknown_error(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=400,
                    json=MagicMock(return_value={})
                )
            )
        )
        api = Api('test')
        api.create('http://localhost/', 'cool')
