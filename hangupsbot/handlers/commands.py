import re, shlex

import hangups

from hangupsbot.utils import text_to_segments
from hangupsbot.handlers import handler, StopEventHandling
from hangupsbot.commands import command


default_bot_alias = '/bot'


def find_bot_alias(aliases_list, text):
    """Return True if text starts with bot alias"""
    command = text.split()[0].lower()
    for alias in aliases_list:
        if alias.lower().startswith('regex:') and re.search(alias[6:], command, re.IGNORECASE):
            return True
        elif command == alias.lower():
            return True
    return False

def is_bot_alias_too_long(text):
    """check whether the bot alias is too long or not"""
    if default_bot_alias in text:
        return True
    else:
        return False


@handler.register(priority=5, event=hangups.ChatMessageEvent)
def handle_command(bot, event):
    """Handle command messages"""
    # Test if message is not empty
    if not event.text:
        return

    # Get list of bot aliases
    aliases_list = bot.get_config_suboption(event.conv_id, 'commands_aliases')
    if not aliases_list:
        aliases_list = [default_bot_alias]

    # Test if message starts with bot alias
    if not find_bot_alias(aliases_list, event.text):
        return

    # Test if command handling is enabled
    if not bot.get_config_suboption(event.conv_id, 'commands_enabled'):
        raise StopEventHandling

    # Parse message
    line_args = shlex.split(event.text, posix=False)

    # Test if command length is sufficient
    if len(line_args) < 2:
        yield from event.conv.send_message(
            text_to_segments(_('{}: 무엇을 도와드릴까요?').format(event.user.full_name))
        )
        raise StopEventHandling

    # Test if user has permissions for running command
    commands_admin_list = command.get_admin_commands(bot, event.conv_id)
    if commands_admin_list and line_args[1].lower() in commands_admin_list:
        admins_list = bot.get_config_suboption(event.conv_id, 'admins')
        if event.user_id.chat_id not in admins_list:
            yield from event.conv.send_message(
                text_to_segments(_('{}: 권한이 없습니다.').format(event.user.full_name))
            )
            raise StopEventHandling

    # Run command
    yield from command.run(bot, event, *line_args[1:])

    #Check whether the bot alias is too long or not
    if is_bot_alias_too_long(event.text):
        yield from event.conv.send_message(
            text_to_segments(_('**Tip**: /bot 대신에 /b, /, ! 등을 사용할 수 있어요'))
        )

    # Prevent other handlers from processing event
    raise StopEventHandling
