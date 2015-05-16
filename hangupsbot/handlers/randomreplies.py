import random

import hangups

from hangupsbot.utils import word_in_text, text_to_segments
from hangupsbot.handlers import handler


def find_keyword(kw, text):
    """Return True if keyword is in text"""
    if kw == "*":
        return True
    elif kw.lower().startswith("regex:") and re.search(kw[6:], text, re.DOTALL | re.IGNORECASE):
        return True
    elif word_in_text(kw, text):
        return True
    elif kw == text:
        return True
    else:
        return False


@handler.register(priority=7, event=hangups.ChatMessageEvent)
def handle_randomreply(bot, event):
    # if the text is in the auto reply list, don't use random reply 
    if bot.get_config_suboption(event.conv_id, 'autoreplies_enabled'):
        # Test if there are actually any autoreplies
        autoreplies_list = bot.get_config_suboption(event.conv_id, 'autoreplies')
        for kwds, sentence in autoreplies_list:
            for kw in kwds:
                if find_keyword(kw, event.text):
                    return

    # Test if randomreplies are enabled
    if not bot.get_config_suboption(event.conv_id, 'randomreplies_enabled'):
        return

    randomreplies_list = bot.get_config_suboption(event.conv_id, 'randomreplies')
    yield from event.conv.send_message(text_to_segments(random.choice(randomreplies_list)))
