import requests
import gease.exceptions as exceptions


MESSAGE_TAG_EXISTS = "Tag already exists"


class Api(object):
    """
    A session holder so that each request shares the same token
    """
    def __init__(self, personal_access_token):
        self.__session = requests.Session()
        self.__session.headers.update({
            'Authorization': 'token %s' % personal_access_token})

    def create(self, url, data):
        """
        Create a release

        More information at:
        https://developer.github.com/v3/repos/releases/#create-a-release
        """
        r = self.__session.post(url, json=data)
        if r.status_code == 201:
            return r.json()
        elif r.status_code == 422:
            raise exceptions.ReleaseExistException(MESSAGE_TAG_EXISTS)
        else:
            raise exceptions.UnhandledException(str(r.status_code))
