import logging


def print_arr(bot, message, arr, with_index=True):
    text = ""
    for i in range(0, len(arr)):
        text += (f"[{i + 1}]" if with_index else "") + f"{arr[i]}\n\n"
    bot.send_message(message.chat.id, text)


def addToLog(text, err_type="message"):
    print(text)
    logging.basicConfig(filename="bot.log", filemode='a')
    logging.warning(text)
