import logging
from ConfigParser import RawConfigParser
from tweepy import api, StreamListener, Stream, BasicAuthHandler


LOG = logging.getLogger('isonatrain')


class Listener(StreamListener):

    __slots__ = ('templates', 'output', 'triggers')

    def __init__(self, templates, output, triggers):
        self.templates = templates
        self.output = output
        self.triggers = triggers

    def on_status(self, status):
        print "%s: %s" % (status.user.screen_name, status.text)


def get_user_ids(screen_names):
    return [user.id for user in api.lookup_users(screen_names=screen_names)]

def read_config(parser):
    auth = dict((k, parser.get('auth', k)) for k in ('username', 'password'))
    templates = dict(parser.items('templates'))
    output = dict(parser.items('output'))
    if sorted(templates.keys()) != sorted(output.keys()):
        raise Exception('Templates and output locations must have same keys.')
    triggers = {}
    for section in parser.sections():
        if section.startswith('@'):
            screen_name = section[1:]
            if screen_name not in output:
                continue
            triggers[screen_name] = dict(parser.items(section))
    if sorted(output.keys()) != sorted(triggers.keys()):
        raise Exception('Must have a trigger section per output location.')
    return auth, templates, output, triggers

def main():
    parser = RawConfigParser()
    parser.read('config.ini')
    auth, templates, output, triggers = read_config(parser)

    stream = Stream(
            BasicAuthHandler(auth['username'], auth['password']),
            Listener(templates, output, triggers),
            secure=True)
    stream.filter(follow=get_user_ids(triggers.keys()))

if __name__ == '__main__':
    main()
