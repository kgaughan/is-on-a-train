import logging
from ConfigParser import RawConfigParser
from tweepy import api, StreamListener, Stream, BasicAuthHandler


LOG = logging.getLogger('isonatrain')


class Listener(StreamListener):
    def on_status(self, status):
        print "%s: %s" % (status.user.screen_name, status.text)


def get_user_ids(screen_names):
    return [user.id for user in api.lookup_users(screen_names=screen_names)]

def stream(username, password, triggers):
    auth = BasicAuthHandler(username, password)
    listener = Listener()
    ids = get_user_ids(triggers.keys())
    Stream(auth, listener, secure=True).filter(follow=ids)

def read_config(parser):
    auth = dict((k, parser.get('auth', k)) for k in ('username', 'password'))
    triggers = {}
    for section in parser.sections():
        if section.startswith('@'):
            screen_name = section[1:]
            triggers[screen_name] = dict(parser.items(section))
    return auth, triggers

def main():
    parser = RawConfigParser()
    parser.read('config.ini')
    auth, triggers = read_config(parser)
    stream(auth['username'], auth['password'], triggers)

if __name__ == '__main__':
    main()
