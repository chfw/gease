import requests
import gease.exceptions as exceptions


class Api(object):
    def __init__(self, token):
        self.__session = requests.Session()
        self.__session.headers.update({
            'Authorization': 'token %s' % token})

    def create(self, url, data):
        r = self.__session.post(url, json=data)
        if r.status_code == 201:
            return r.json()
        elif r.status_code == 422:
            message = "Tag already exists"
            raise exceptions.ReleaseExistException(message)
        else:
            raise Exception("failed")
