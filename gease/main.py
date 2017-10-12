import os
import sys
import json
import crayons
from gease._version import __version__, __description__
from gease.release import EndPoint
import gease.exceptions as exceptions
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

DEFAULT_RELEASE_MESSAGE = "A new release via gease."
HELP = """%s. version %s

Usage: %s

where:

   release message could be a quoted string or space separate string

Examples:

   gs gease v0.0.1 first great release
   gs gease v0.0.2 "second great release"
""" % (
    crayons.yellow('gease ' + __description__),
    crayons.magenta(__version__, bold=True),
    crayons.yellow('gs repo tag [release message]', bold=True),
)


def main():
    user, token = get_token()
    if len(sys.argv) < 3:
        if len(sys.argv) == 2:
            print('Error: %s' % crayons.red('Not enough arguments'))
        print(HELP)
        sys.exit(-1)
    repo = sys.argv[1]
    tag = sys.argv[2]
    msg = " ".join(sys.argv[3:])
    if len(msg) == 0:
        msg = DEFAULT_RELEASE_MESSAGE
    release = EndPoint(token, user, repo)
    try:
        url = release.publish(tag_name=tag, name=tag, body=msg)
        print('Release is created at: %s' % crayons.green(url))
    except exceptions.ReleaseExistException as e:
        print('Error: %s' % crayons.red(str(e)))


def get_token():
    """
    Find geasefile from user's home folder
    """
    home_dir = os.path.expanduser('~')
    geasefile = os.path.join(home_dir, '.gease')
    try:
        with open(geasefile, 'r') as config:
            gease = json.load(config)
            return gease['user'], gease['personal_token']
    except FileNotFoundError:
        raise exceptions.NoGeaseConfigFound(
            'Cannot find %s' % geasefile)


if __name__ == '__main__':
    main()
