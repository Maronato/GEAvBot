from senpaibot.communication.basic import markdown_message, custom_keyboard
from senpaibot.menu.keyboards import eliminate_keyboard
from senpaibot.subscriptions.subscription import Subscription
from senpaibot.reading.reading import user_stats
from senpaibot.database.chat_api import get_chat, set_chat


def is_plural(plural):
    return 's' if plural else ''


def is_plural_is(plural):
    return 'são' if plural else 'é'


def start(chat_id, extra_info=False, group=False):
    response = """
*"Como fazer Senpai me notar?"*

Essa é uma pergunta que você costuma fazer?
Senpai é difícil de conquistar, mas tem uma queda por conhecimentos de programação!

Eu te ajudarei a ficar #foda em tudo programação para que o coração dele seja seu

*Comandos*
/eliminar - Elimine capítulos já lidos
/lembretes - Controle seus lembretes
/info - Veja suas estatísticas de leitura
/ajuda - Obter ajuda
    """
    if extra_info and get_chat(chat_id) is None:
        data = {'chat_id': {'S': str(chat_id)}, 'extra': {'M': extra_info}}
        set_chat(chat_id, data)
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def help(chat_id, group=False):
    response = """
*Ajuda*

A lista de comandos disponíveis é:
*Comandos*
/eliminar - Elimine capítulos já lidos
/lembretes - Controle seus lembretes
/info - Veja suas estatísticas de leitura
/ajuda - Obter ajuda

Se precisar de suporte, entre em contato com o desenvolvedor:
@Maronato
    """
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def info(chat_id, group=False):

    stats = user_stats(chat_id)
    response = f"""
*Estatísticas*

Você já leu {stats['read_count']} capítulo{is_plural(not stats['read_count'] == 1)} e está com {stats['late_count']} capítulo{is_plural(not stats['late_count'] == 1)} acumulado{is_plural(not stats['late_count'] == 1)}.
    """
    if stats['late_count'] > 0:
        if stats['late_count'] > 1:
            plural = True
        else:
            plural = False
        response += f"""

Seu{is_plural(plural)} capítulo{is_plural(plural)} acumulado{is_plural(plural)} {is_plural_is(plural)}:
"""
    for cap in stats['late']:
        response += f"""
*{cap}*
    """
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def eliminar(chat_id):
    eliminate_keyboard(chat_id)


def lembretes(chat_id):
    Subscription(chat_id).interact()


def unknown(chat_id, group=False):
    response = "Não reconheço esse comando :(\n\n/ajuda - Lista de comandos"
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def keyboard(group):
    if not group:
        reply_markup = custom_keyboard()
    else:
        reply_markup = None
    return reply_markup
