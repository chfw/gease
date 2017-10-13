from gease.rest import Api
from gease.uritemplate import UriTemplate
import gease.exceptions as exceptions


RELEASE_URL = 'https://api.github.com/repos{/owner}{/repo}/releases'
KEY_HTML_URL = 'html_url'
MESSAGE_MISSING_KEY = 'No %s in github repsonse' % KEY_HTML_URL


class EndPoint(object):
    """
    Github release endpoint

    More documentation is available at
    https://developer.github.com/v3/repos/releases/
    """
    def __init__(self, token, owner, repo):
        self.__template = UriTemplate(RELEASE_URL)
        self.__template.owner = owner
        self.__template.repo = repo
        self.__client = Api(token)

    @property
    def url(self):
        return str(self.__template)

    def publish(self, **kwargs):
        """
        Publish the release

        :returns: the url to the release on github
        :throws: exception if gihub changes its api response
        """
        try:
            json_reply = self.__client.create(self.url, kwargs)
            return json_reply[KEY_HTML_URL]
        except KeyError:
            raise exceptions.AbnormalGithubResponse(
                MESSAGE_MISSING_KEY)
