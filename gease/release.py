from gease.rest import Api
from gease.uritemplate import UriTemplate
import gease.exceptions as exceptions


RELEASE_URL = 'https://api.github.com/repos{/owner}{/repo}/releases'


class EndPoint(object):
    def __init__(self, token, owner, repo):
        self.__template = UriTemplate(RELEASE_URL)
        self.__template.owner = owner
        self.__template.repo = repo
        self.__client = Api(token)

    @property
    def url(self):
        return str(self.__template)

    def publish(self, **kwargs):
        try:
            json_reply = self.__client.create(self.url, kwargs)
            return json_reply['html_url']
        except KeyError:
            raise exceptions.AbnormalGithubResponse(
                'No html_url in github repsonse')
