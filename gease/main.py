import os
import sys
import json
import crayons
from gease.release import EndPoint
import gease.exceptions as exceptions

DEFAULT_RELEASE_MESSAGE = "A new release via gease."


def get_token():
    home_dir = os.path.expanduser('~')
    geasefile = os.path.join(home_dir, '.gease')
    try:
        with open(geasefile, 'r') as config:
            gease = json.load(config)
            return gease['user'], gease['personal_token']
    except FileNotFoundError:
        raise exceptions.NoGeaseConfigFound(
            'Cannot find %s' % geasefile)


def main():
    user, token = get_token()
    repo = sys.argv[1]
    tag = sys.argv[2]
    msg = " ".join(sys.argv[3:])
    if len(msg) == 0:
        msg = DEFAULT_RELEASE_MESSAGE
    release = EndPoint(token, user, repo)
    try:
        url = release.publish(tag_name=tag, name=tag, body=msg)
        print('Release is created at: %s' % url)
    except exceptions.ReleaseExistException as e:
        print(crayons.red(str(e)))


if __name__ == '__main__':
    main()
