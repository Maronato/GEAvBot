from senpaibot.database.subscriptions_api import get_subscription, set_subscription
from senpaibot.communication.basic import inline_keyboard_message, edit_message, answer_callback_query
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import emoji


BASE_SUBS = subs = {
    'late': False,  # Todos os atrasados
    'beginweek': False,  # Semana atual, no dia que começa
    'midweek': False,   # Atual, no meio da semana
    'finalweek': False  # Atual, no fim da semana
}


class Subscription:
    """docstring for Subscription."""

    def __init__(self, chat_id, callback=False, message_id=False, extra_info={'S': ""}):
        self.chat_id = chat_id
        self.message_id = message_id
        self.callback = callback
        self.extra_info = extra_info

    def update_subscription(self, changed):
        subs = self.subs
        subs[changed] = not subs[changed]
        set_subscription(self.chat_id, subs, extra=self.extra_info)
        self.get_subs()
        return self

    def interact(self):
        sender_method = edit_message if self.callback else inline_keyboard_message
        sender_method(*self.menu_tuple)
        if self.callback:
            answer_callback_query(self.callback)
        return self

    def get_subs(self):
        subs = get_subscription(self.chat_id)
        # Create a new one if the user is new
        if not subs:
            subs = BASE_SUBS
        self.loadedsubs = subs
        return self

    @property
    def menu_tuple(self):
        message = """*Lembretes*\n
Toque em um lembrete para se inscrever\n
Toque novamente para se desinscrever.\n
A opção 'Atrasados' te avisa na segunda de todos os capítulos atrasados.\n
As outras opções te avisam do próximo capítulo que você tem que ler no começo, meio e fim da semana.
"""

        subs = self.subs
        sub_sign = emoji.emojize(':white_heavy_check_mark:  ', use_aliases=True)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=(sub_sign if subs['late'] else '') + 'Atrasados', callback_data='sub.late'),
                InlineKeyboardButton(text=(sub_sign if subs['beginweek'] else '') + 'Início', callback_data='sub.beginweek')
            ],
            [
                InlineKeyboardButton(text=(sub_sign if subs['midweek'] else '') + 'Meio', callback_data='sub.midweek'),
                InlineKeyboardButton(text=(sub_sign if subs['finalweek'] else '') + 'Final', callback_data='sub.finalweek')
            ],
        ])
        response_id = self.message_id or self.chat_id
        return [response_id, message, keyboard]

    @property
    def subs(self):
        subs = getattr(self, "loadedsubs", False)
        if not subs:
            self.get_subs()
        return self.loadedsubs
