from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from senpaibot.reading.reading import undated_late, dated_remaining_not_late
from senpaibot.database.reading_api import get_reading, eliminate_chapter

from senpaibot.communication.basic import edit_message, answer_callback_query, inline_keyboard_message


def get_eliminate_list(chat_id):
    read_list = get_reading(chat_id)
    remaining = dated_remaining_not_late(read_list)
    late = undated_late(read_list)
    available = [f"{chap} - Atrasado" for chap in late][:5]
    available.extend([f"{i[0]} - {i[1].strftime('%d/%m')}" for i in remaining][:5])
    return available[:5]


def get_eliminate_list_name_only(chat_id):
    el_list = get_eliminate_list(chat_id)
    return [chap.split(' - ')[0] for chap in el_list]


def eliminate_keyboard(chat_id, message_id=None, query_id=False):
    message = "*Eliminar capítulos*\n\nToque um capítulo para eliminá-lo/marcar como lido."
    available = get_eliminate_list(chat_id)
    if len(available) == 0:
        message = "*Eliminar capítulos*\n\nVocê terminou tudo :)"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=f'eliminate.{i}')]
        for i, text in enumerate(available)
    ])
    if query_id:
        edit_message(message_id, message, keyboard)
        answer_callback_query(query_id)
    else:
        inline_keyboard_message(chat_id, message, keyboard)


def check_eliminate_keyboard(chat_id, chapter, message_id, query_id):
    el_list = get_eliminate_list_name_only(chat_id)
    response = "*Tem certeza?*\n\nVocê está prestes a eliminar '" + el_list[int(chapter)] + "' e não há como reverter essa decisão!"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Eliminar', callback_data='eliminate.' + str(chapter) + '.y')],
        [InlineKeyboardButton(text='<< Voltar', callback_data='eliminate')],
    ])
    edit_message(message_id, response, keyboard)
    answer_callback_query(query_id)


def eliminate_complete_keyboard(chat_id, chapter, option, message_id, query_id):
    el_list = get_eliminate_list_name_only(chat_id)
    el_name = el_list[int(chapter)]
    eliminate_chapter(chat_id, el_name)
    response = '\n\n'.join(["*Pronto!*", f"{el_name} eliminado!"])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='<< Voltar', callback_data='eliminate')],
    ])
    edit_message(message_id, response, keyboard)
    answer_callback_query(query_id)
