import logging
from tweepy import api, StreamListener, Stream, BasicAuthHandler


LOG = logging.getLogger('isonatrain')


class Listener(StreamListener):
    def on_status(self, status):
        print "%s: %s" % (status.user.screen_name, status.text)


def get_user_ids(screen_names):
    return [user.id for user in api.lookup_users(screen_names=screen_names)]

def stream(username, password, to_follow):
    auth = BasicAuthHandler(username, password)
    listener = Listener()
    ids = get_user_ids(to_follow)
    Stream(auth, listener, secure=True).filter(follow=ids)

def main():
    username = 'talideon'
    password = ''
    to_follow = [username]
    stream(username, password, to_follow)

if __name__ == '__main__':
    main()
