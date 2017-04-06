import json
from slackclient import SlackClient
import tweepy


def get_accounts(name: str):
    f = open('config/account/%s.json' % name)
    return json.load(f)


def get_slack_client(team: str):
    token = get_accounts('slack')[team]['token']
    return SlackClient(token)


def get_twitter_auth(user_name: str):
    tokens = get_accounts('twitter')
    keys = tokens[user_name]
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['acccess_token'], keys['acccess_token_secret'])
    return auth


def get_twitter_api(user_name: str):
    auth = get_twitter_auth(user_name)
    return tweepy.API(auth_handler=auth)


def post_to_twitter(user_name: str, text: str):
    api = get_twitter_api(user_name)
    api.update_status(text)


def unfold_tweet_entities(status):
    if('extended_entities' in status._json.keys()):
        replace = ''
        link = ''
        for item in status.extended_entities['media']:
            replace = item['url']
            link = link + ' ' + item['media_url_https']
        return status.text.replace(replace, link)
    else:
        return status.text


def tweet_to_slack(team: str, channel: str, status):
    sc = get_slack_client(team)
    sc.api_call(
        "chat.postMessage",
        channel=get_accounts('slack')[team]['channels'][channel],
        text=unfold_tweet_entities(status),
        username=status.author.name,
        icon_url=status.author.profile_image_url_https
    )


def like_to_slack(team: str, status):
    sc = get_slack_client(team)
    text = status.target_object['text']
    if('extended_entities' in status.target_object):
        replace = ''
        link = ''
        for item in status.target_object['extended_entities']['media']:
            replace = item['url']
            link = link + ' ' + item['media_url_https']
            text = text.replace(replace, link)
    sc.api_call(
        "chat.postMessage",
        channel=get_accounts('slack')[team]['channels']['like'],
        text=text,
        username=status.target['name'],
        icon_url=status.target['profile_image_url_https']
    )


def post_message_to_slack(team, channel, user_name, icon_emoji, text, attachments=[]):
    sc = get_slack_client(team)
    sc.api_call(
        "chat.postMessage",
        channel=get_accounts('slack')[team]['channels'][channel],
        text=text,
        username=user_name,
        icon_emoji=icon_emoji,
        attachments=json.dumps(attachments)
    )


def log(username: str, icon_emoji: str, text: str):
    post_message_to_slack(
        'TEAM_NAME',
        'log',
        username,
        icon_emoji,
        text
    )


def test(username: str, icon_emoji: str, text: str, attachments=[]):
    post_message_to_slack(
        'TEAM_NAME',
        'test',
        username,
        icon_emoji,
        text,
        attachments
    )
