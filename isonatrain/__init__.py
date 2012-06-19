from tweepy import api
import httplib


def get_user_ids(screen_names):
    return [user.id for user in api.lookup_users(screen_names=screen_names)]

def main():
    print get_user_ids(['talideon'])

if __name__ == '__main__':
    main()
