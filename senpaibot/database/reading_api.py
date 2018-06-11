import json
from .dynamo_db import setkey, get_all
from .chat_api import get_chat


def get_reading(chat_id):
    chat = get_chat(chat_id)
    if chat is not None:
        chat = chat.get('reading', {})
        return json.loads(chat.get('S', '[]'))
    return {'chat_id': {'S': str(chat_id)}, 'reading': {'S': '[]'}}


def set_reading(chat_id, reading, extra={'S': ""}):
    chat = get_chat(chat_id)
    if not chat.get('reading', False):
        chat['reading'] = {}
    chat['reading']['S'] = json.dumps(reading)
    if extra.get('S'):
        chat['extra']['M'] = extra
    return setkey(chat_id, chat)


def eliminate_chapter(chat_id, chapter):
    reading = get_reading(chat_id)
    reading.append(chapter)
    set_reading(chat_id, reading)


def get_all_readings():
    users = get_all()
    all_reads = []
    for user in users['Items']:
        try:
            c_id = int(user['chat_id']['S'])
            n_reading = json.loads(user['reading']['S'])
            try:
                extra = user['extra']['M']
                all_reads.append({"id": c_id, "reading": n_reading, "extra": extra})
            except KeyError as e:
                all_reads.append({"id": c_id, "reading": n_reading})
                print("INFO User {} does not have Extra info".format(c_id))
        except Exception as e:
            print("ERROR: ", e.__class__, e)
    return all_reads
