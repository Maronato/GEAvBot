from datetime import datetime, timedelta
from senpaibot.reading.reading import dated_late, dated_remaining


def compose_message(read_list, reminder, hours_delta, days_delta):
    dt = datetime.now() + timedelta(days=days_delta, hours=hours_delta)
    late = dated_late(read_list, lambda: dt)
    remaining = dated_remaining(read_list)
    if reminder == 'late':
        late = list(late)
        if len(late) > 0:
            message = f"""
*Você tem capítulos acumulados!*

Eles são:
            """
            for l in late:
                message += f"""
*{l[0]}*
"""
            return message
    else:
        remaining = list(remaining)
        if len(remaining) > 0:
            starter = {
                'beginweek': '*A semana tá começando*, mas não esqueça do capítulo que você tem que ler!\n\nDessa vez é o ',
                'midweek': '*Tá no meio da semana e esse capítulo tá te esperando*\n\nNão esquece de ler o ',
                'finalweek': '*Semana chegando ao fim*, mas tem capítulo na fila!\n\nCorre agora e abre o '
            }
            message = starter[reminder] + f"*{remaining[0][0]}*"
            if remaining[0][1] < datetime.now() - timedelta(days=1):
                message += f' que já está atrasado {int((datetime.now() - remaining[0][1]).days)} dias!'
            else:
                message += f" para o dia *{remaining[0][1].strftime('%d de %b')}*"
            return message
    return False


def get_reminders(chats, reminders, hours_delta=0, days_delta=0):
    for chat in chats:
        for reminder in reminders:
            if chat.get('sub', {}).get(reminder, False):
                message = compose_message(chat['reading'], reminder, hours_delta, days_delta)
                if message:

                    chat['reminders'] = chat.get('reminders', {})
                    chat['reminders'][reminder] = message
    return chats
