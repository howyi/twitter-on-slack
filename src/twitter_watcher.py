import account
import sys
import tweepy

user_name = sys.argv[1]

team = 'TEAM_NAME'

auth = account.get_twitter_auth(user_name)
api = tweepy.API(auth_handler=auth)
my_screen_name = api.me().screen_name


def log(text):
    account.log('twitter_watcher(%s)' % user_name, ':snake:', text)


def send_status(status):
    if hasattr(status, 'retweeted_status'):
        status = status.retweeted_status
    account.tweet_to_slack(team, user_name, status)


def is_like(status):
    return 'favorite' == status.event \
        and my_screen_name == status.source['screen_name']


class listener(tweepy.StreamListener):

    def on_status(self, status):
        send_status(status)

    def on_event(self, status):
        if is_like(status):
            account.like_to_slack(team, status)

    def on_error(self, status):
        log(status)

if __name__ == '__main__':
    log('twitter watcher started')
    stream = tweepy.Stream(auth, listener())
    stream.userstream()
