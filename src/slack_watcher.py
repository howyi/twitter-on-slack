import account
import time

team = 'TEAM_NAME'
sc = account.get_slack_client(team)
slack_user_id = sc.api_call("auth.test")['user_id']
start_time = time.time()
channels = account.get_accounts('slack')[team]['channels']


def log(text):
    account.log('slack_watcher(%s)' % team, ':snake:', text)


def is_message(event):
    if 'message' == event['type'] and 'user' in event:
        return slack_user_id == event['user'] \
            and start_time < float(event['ts'])
    else:
        return False


def event_switch(event):
    if is_message(event):
        if event['channel'] == channels['TWITTER_ID']:
            account.post_to_twitter('TWITTER_ID', event['text'])

if __name__ == '__main__':
    log('slack watcher started.')
    sc.rtm_connect()
    while True:
        for event in sc.rtm_read():
            event_switch(event)
        time.sleep(1)
