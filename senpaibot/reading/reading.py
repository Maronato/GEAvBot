from .reading_list import get_default_list
from senpaibot.database import reading_api
from datetime import datetime, timedelta

default_list = get_default_list()


def undated_remaining(read_list):
    read_set = set(read_list)
    undated_reading_set = default_list.undated_reading_set
    to_read = undated_reading_set - read_set
    return to_read


def dated_remaining(read_list):
    to_read = undated_remaining(read_list)
    reading_list = default_list.reading_list
    return filter(lambda item: item[0] in to_read, reading_list)


def dated_late(read_list, date=datetime.now):
    remaining = dated_remaining(read_list)
    return filter(lambda item: item[1] < date() - timedelta(days=1), remaining)


def undated_late(read_list, date=datetime.now):
    remaining = dated_remaining(read_list)
    return [chap[0] for chap in filter(lambda item: item[1] < date() - timedelta(days=1), remaining)]


def dated_remaining_not_late(read_list, date=datetime.now):
    return filter(lambda rem: rem not in dated_late(read_list, date), dated_remaining(read_list))


def user_stats(chat_id, date=datetime.now):
    read_list = reading_api.get_reading(chat_id)
    read_count = len(read_list)
    late = undated_late(read_list, date)
    late_count = len(late)
    return {
        'read_count': read_count,
        'late_count': late_count,
        'late': late
    }
