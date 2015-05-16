import re

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

def is_image(text):
    """Return True if the text contains image extension"""
    if "jpg" in text:
        return True
    elif "jpeg" in text:
        return True
    elif "gif" in text:
        return True
    elif "png" in text:
        return True
    else:
        return False

@handler.register(priority=7, event=hangups.ChatMessageEvent)
def handle_autoreply(bot, event):
    """Handle autoreplies to keywords in messages"""
    # Test if message is not empty
    if not event.text:
        return

    # Test if autoreplies are enabled
    if not bot.get_config_suboption(event.conv_id, 'autoreplies_enabled'):
        return

    # Test if there are actually any autoreplies
    autoreplies_list = bot.get_config_suboption(event.conv_id, 'autoreplies')
    if not autoreplies_list:
        return

    for kwds, sentence in autoreplies_list:
        for kw in kwds:
            if find_keyword(kw, event.text):
                if not is_image(sentence):
                    yield from event.conv.send_message(text_to_segments(sentence))
                    return
                else:
                    image_id_list = yield from bot.upload_images([sentence])
                    yield from event.conv.send_message([], image_id=image_id_list[0])
                    return
