from senpaibot.database.subscriptions_api import get_all_subscriptions
from telepot.exception import BotWasBlockedError

from senpaibot.database.chat_api import delete_chat
from senpaibot.communication.basic import markdown_message
from senpaibot.reading.reminders import get_reminders

import os


class SubscriptionSender:
    """docstring for SubscriptionSender."""

    def __init__(self, reminder, debug=False, hours_delta=-3, debug_days_delta=0):
        self.reminder = reminder
        self.debug = debug
        self.hours_delta = hours_delta
        self.debug_days_delta = debug_days_delta

        print(reminder, debug)

        if reminder == "beginweek":
            self.reminders = ["late", "beginweek"]
        elif reminder == "midweek":
            self.reminders = ["midweek"]
        else:
            self.reminders = ["finalweek"]

    titles = {
        "late": "*Você tem capítulos acumulados!*\n\n",
        "beginweek": "*O capítulo dessa semana é:*\n\n",
        "midweek": "*Você já começou a ler?*\n\n",
        "finalweek": "*Tá quase no fim da semana!*\n\n"
    }

    def send(self):
        chats = get_all_subscriptions()
        if self.debug:
            chats = list(filter(lambda x: str(x['id']) == str(os.environ.get("DEV_CHAT_ID")), chats))

        print(len(chats), "chats selected")

        chats = get_reminders(chats, reminders=self.reminders, hours_delta=self.hours_delta, days_delta=self.debug_days_delta)
        for k, chat in enumerate(chats):
            if chat.get('reminders', False):
                for reminder, message in chat['reminders'].items():
                    # Try to send
                    try:
                        # Get user-specific message data
                        markdown_message(chat['id'], message)
                    except BotWasBlockedError as e:
                        try:
                            if chat['extra']['chat_type']['S'] == 'private':
                                username = chat['extra']['username']['S']
                                name = chat['extra']['first_name']['S'] + " " + chat['extra']['last_name']['S']
                                info = "User {}({}) with ID {} blocked the bot and is being removed from the table".format(name, username, chat['id'])
                            elif chat['extra']['chat_type']['S'] == 'group':
                                group_name = chat['extra']['first_name']['S']
                                info = "Group {} with ID {} blocked the bot and is being removed from the table".format(group_name, chat['id'])
                        except KeyError:
                            info = "Unknown with ID {} blocked the bot and is being removed from the table".format(chat['id'])

                        # Log error
                        print("EXCEPTION: ", info)
                        delete_chat(chat['id'])
                    except Exception as e:

                        # Log error
                        print("EXCEPTION: An error has occured when sending sub notification to chat ID {}:\n{}".format(chat['id'], e))
