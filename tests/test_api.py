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


@patch('gease.rest.requests.Session')
def test_create(fake_session):
    fake_session.return_value = MagicMock(
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
@patch('gease.rest.requests.Session')
def test_existing_release(fake_session):
    fake_session.return_value = MagicMock(
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
@patch('gease.rest.requests.Session')
def test_unknown_error(fake_session):
    fake_session.return_value = MagicMock(
        post=MagicMock(
            return_value=MagicMock(
                status_code=400,
                json=MagicMock(return_value={})
                )
            )
        )
    api = Api('test')
    api.create('http://localhost/', 'cool')
