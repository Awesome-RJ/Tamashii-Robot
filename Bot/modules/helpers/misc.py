from typing import List, Dict

from telegram import MAX_MESSAGE_LENGTH, InlineKeyboardButton, Bot, ParseMode
from telegram.error import TelegramError



class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def split_message(msg: str) -> List[str]:
    if len(msg) < MAX_MESSAGE_LENGTH:
        return [msg]

    lines = msg.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < MAX_MESSAGE_LENGTH:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    # Else statement at the end of the for loop, so append the leftover string.
    result.append(small_msg)

    return result


def paginate_modules(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__mod_name__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        ) if chat else sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_module({})".format(
                        prefix, x.__mod_name__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    pairs = []
    pair = []

    for module in modules:
        pair.append(module)
        if len(pair) > 2:
            pairs.append(pair)
            pair = []

    if pair:
        pairs.append(pair)

    # pairs = [
    #     modules[i * 3:(i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)
    # ]

    # round_num = len(modules) / 3
    # calc = len(modules) - round(round_num)
    # if calc == 1:
    #     pairs.append((modules[-1], ))
    # elif calc == 2:
    #     pairs.append((modules[-1], ))

    # max_num_pages = ceil(len(pairs) / 28)
    # modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side

    #if len(pairs) > 21:
    #    pairs = pairs[modulo_page * 28:28]
    # else:
    #     pairs += [[
    #         EqInlineKeyboardButton(tld(chat_id, 'btn_go_back'),
    #                                callback_data="bot_start")
    #     ]]

    return pairs


def send_to_list(
    bot: Bot, send_to: list, message: str, markdown=False, html=False
) -> None:
    if html and markdown:
        raise Exception("Can only send with either markdown or HTML!")
    for user_id in set(send_to):
        try:
            if markdown:
                bot.send_message(user_id, message, parse_mode=ParseMode.MARKDOWN)
            elif html:
                bot.send_message(user_id, message, parse_mode=ParseMode.HTML)
            else:
                bot.send_message(user_id, message)
        except TelegramError:
            pass  # ignore users who fail
