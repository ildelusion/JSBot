from hangups.ui.utils import get_conv_name

from hangupsbot.utils import text_to_segments
from hangupsbot.commands import command


@command.register_unknown
def unknown_command(bot, event, *args):
    """Unknown command handler"""
    yield from event.conv.send_message(
        text_to_segments(_('{}: \n존재하지 않는 명령입니다.\n'
                         + '도움말을 보려면 "/bot help"를 입력하세요.')
                         .format(event.user.full_name))
    )

@command.register
def help(bot, event, cmd=None, *args):
    """사용법: /bot help [command]"""
    cmd = cmd if cmd else 'help'
    try:
        command_fn = command.commands[cmd]
    except KeyError:
        yield from command.unknown_command(bot, event)
        return

    text = _('**{}:**\n'
             '{}').format('도움말', _(command_fn.__doc__))

    if cmd == 'help':
        text += _('\n\n'
                  '**지원되는 명령어 목록:**\n'
                  '{}').format(', '.join(sorted(command.commands.keys())))

    yield from event.conv.send_message(text_to_segments(text))

@command.register
def ping(bot, event, *args):
    """Let's play ping pong!"""
    yield from event.conv.send_message(text_to_segments('pong'))

@command.register
def 핑(bot, event, *args):
    """한글 버전의 핑퐁입니다."""
    yield from event.conv.send_message(text_to_segments('퐁'))

@command.register
def echo(bot, event, *args):
    """사용법: /bot echo text"""
    yield from event.conv.send_message(text_to_segments(' '.join(args)))

@command.register(admin=True)
def quit(bot, event, *args):
    """calab bot을 종료합니다."""
    print(_('HangupsBot killed by user {} from conversation {}').format(
        event.user.full_name,
        get_conv_name(event.conv, truncate=True)
    ))
    yield from event.conv.send_message(text_to_segments(_('으앙 쥬금 ㅠ')))
    yield from bot._client.disconnect()
