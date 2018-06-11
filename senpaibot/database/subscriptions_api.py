import json
from .dynamo_db import setkey, get_all
from .chat_api import get_chat


def get_subscription(chat_id):
    from senpaibot.subscriptions.subscription import BASE_SUBS
    sub = get_chat(chat_id)
    if sub is not None:
        data = sub.get('sub', {'S': json.dumps(BASE_SUBS)})['S']
        return json.loads(data)
    return sub


def set_subscription(chat_id, sub, extra={'S': ""}):
    chat = get_chat(chat_id)
    if not chat.get('sub', False):
        chat['sub'] = {}
    chat['sub']['S'] = json.dumps(sub)
    if extra.get('S'):
        chat['extra']['M'] = extra
    return setkey(chat_id, chat)


def get_all_subscriptions():
    subs = get_all()
    all_subs = []
    for sub in subs['Items']:
        try:
            c_id = int(sub['chat_id']['S'])
            n_sub = json.loads(sub['sub']['S'])
            n_read = json.loads(sub.get('reading', {}).get('S', '[]'))
            try:
                extra = sub['extra']['M']
                all_subs.append({"id": c_id, "sub": n_sub, "reading": n_read, "extra": extra})
            except KeyError as e:
                all_subs.append({"id": c_id, "reading": n_read, "sub": n_sub})
                print("INFO User {} does not have Extra info".format(c_id))
        except Exception as e:
            print("ERROR: ", e.__class__, e)
    return all_subs
