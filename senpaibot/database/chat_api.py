from .dynamo_db import getkey, deletekey, setkey


def get_chat(chat_id):
    key = {'chat_id': {'S': str(chat_id)}}
    try:
        return getkey(key)['Item']
    except (KeyError, TypeError):
        return None


def set_chat(chat_id, data):
    setkey(chat_id, data)


def delete_chat(chat_id):
    key = {'chat_id': {'S': str(chat_id)}}
    return deletekey(key)
