"""
A daemon that tracks the tweets of people on Twitter, generating HTML pages
bases on certain trigger phrases containing a matching piece of text.
"""


from ConfigParser import RawConfigParser
import logging
import os.path
import sys
import httplib

import pystache
import tweepy


__version__ = '1.1.0'
__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'


USAGE = "Usage: %s <config>"

LOG = logging.getLogger(__name__)


class Listener(tweepy.StreamListener):
    """
    Reacts to events from the Streaming API.
    """

    __slots__ = ('templates', 'output', 'triggers')

    def __init__(self, templates, output, triggers):
        super(Listener, self).__init__()
        self.templates = templates
        self.output = output
        self.triggers = triggers

    def on_status(self, status):
        screen_name = status.user.screen_name
        LOG.info("Received status '%s' from '%s'", status.text, screen_name)
        if screen_name not in self.triggers:
            return
        text = status.text.lower()
        for trigger, message in self.triggers[screen_name].iteritems():
            if text.find(trigger) != -1:
                LOG.info("Trigger was '%s'; rendering '%s'", trigger, message)
                self.render(screen_name, message)
                LOG.info("Rendering complete")
                break

    def render(self, screen_name, message):
        """
        Generates an output file for the given screen name with the given
        message and writes it to disc.
        """
        page = pystache.render(self.templates[screen_name], message=message)
        with open(self.output[screen_name], 'w+') as fh:
            fh.write(page)


def get_user_ids(api, screen_names):
    """
    Queries Twitter for the User IDs corresponding to the given screen names.
    """
    return [user.id for user in api.lookup_users(screen_names=screen_names)]


def read_config(parser):
    """
    Extract the configuration from a parsed configuration file, checking that
    the data contained within is valid.
    """
    keys = (
        'consumer_key',
        'consumer_secret',
        'access_token_key',
        'access_token_secret',
    )
    auth = dict((k, parser.get('auth', k)) for k in keys)
    templates = dict(parser.items('templates'))
    output = dict(parser.items('output'))
    if sorted(templates.keys()) != sorted(output.keys()):
        raise Exception('Templates and output locations must have same keys.')
    triggers = {}
    for section in parser.sections():
        if section.startswith('@'):
            screen_name = section[1:]
            if screen_name not in output:
                LOG.info(
                    "Screen name '%s' has not template. Ignoring.",
                    screen_name)
                continue
            LOG.info("Adding triggers for '%s'", screen_name)
            triggers[screen_name] = dict(parser.items(section))
    if sorted(output.keys()) != sorted(triggers.keys()):
        raise Exception('Must have a trigger section per output location.')
    return auth, templates, output, triggers


def load_templates(template_paths):
    """
    Loads all the mustache templates for the given users into memory.
    """
    templates = {}
    for name, path in template_paths.iteritems():
        with open(path, 'r') as fh:
            templates[name] = fh.read()
    return templates


def tweak_paths(base, path_dict):
    """
    Tweak paths extracted from a configuration file to make them relative to
    that configuration file.
    """
    result = {}
    for key, path in path_dict.iteritems():
        result[key] = os.path.join(base, path)
    return result


def main():
    """
    Execute the daemon.
    """
    if len(sys.argv) != 2:
        print >> sys.stderr, USAGE % os.path.basename(sys.argv[0])
        return 1

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

    parser = RawConfigParser()
    parser.read(sys.argv[1])
    auth, template_paths, output, triggers = read_config(parser)

    # Tweak the paths to make them relative to the config file.
    base = os.path.dirname(sys.argv[1])
    template_paths = tweak_paths(base, template_paths)
    output = tweak_paths(base, output)

    templates = load_templates(template_paths)

    auth_handler = tweepy.OAuthHandler(
        auth['consumer_key'],
        auth['consumer_secret'])
    # XXX: If these are none, do the OAuth dance.
    auth_handler.set_access_token(
        auth['access_token_key'],
        auth['access_token_secret'])

    LOG.info("Initialising stream...")
    api = tweepy.API(auth_handler)
    stream = tweepy.Stream(
        auth_handler,
        Listener(templates, output, triggers),
        secure=True)
    try:
        LOG.info("Running filter")
        stream.filter(follow=get_user_ids(api, triggers.keys()))
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
