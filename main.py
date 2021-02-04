import config
import telebot
import functions as Fun
import PersonModel
import datetime as dt
import Excel
import time
import os

bot = telebot.TeleBot(config.TOKEN)

group = []
selected = []


def send_commands(message):
    Fun.print_arr(bot, message, config.COMMANDS, False)


def check_message_type(message, message_type="text"):
    if message.content_type == message_type:
        return True
    bot.send_message(message.chat.id, config.REPLICAS["input_err"])
    return False


def load_group_res():
    global selected
    selected = PersonModel.load_marked_on(dt.date.today().day, dt.date.today().month, dt.date.today().year)
    global group
    group = PersonModel.load_all_names()


def send_group(message):
    load_group_res()
    if len(group) == 0:
        bot.send_message(message.chat.id, "Список группы пуст")
        return
    text = ""
    i = 1
    for person in group:
        text += f"[{i}] {person['name']}\n\n"
        i += 1
    bot.send_message(message.chat.id, text)


def send_selected(message):
    load_group_res()
    if len(selected) == 0:
        return
    text = ""
    for person in selected:
        text += f"{person['name']}\n\n"
    bot.send_message(message.chat.id, text)


def admin_logic(message):
    is_nums = False
    data = []
    if check_message_type(message, "document"):
        file_info = bot.get_file(message.document.file_id)
        file = bot.download_file(file_info.file_path).decode("utf-8")
        data = list(map(str, file.split('\r\n')))
        PersonModel.delete_all_persons()
    elif check_message_type(message):
        try:
            input_data = list(map(int, message.text.split(" ")))
            data = []
            for index in input_data:
                data.append(group[index - 1]["id"])
            is_nums = True
        except Exception as e:
            Fun.addToLog(e.args, "ERROR")
            is_nums = False
            try:
                data = list(map(str, message.text.split("*")))
            except Exception as e:
                print(e.args)
                return

    bot.send_message(message.chat.id, "Ожидайте выполнения запроса")
    if is_nums:
        PersonModel.delete_by_arr_of_id(data)
    else:
        for person in data:
            PersonModel.add_in_list(person)
    send_group(message)


def admin_namespace(message):
    if check_message_type(message):
        try:
            data = list(map(str, message.text.split(" ")))
        except Exception as e:
            Fun.addToLog(e.args, "ERROR")
            return
        if data[0] == config.ADMIN["LOGIN"] and data[1] == config.ADMIN["PASSWORD"]:
            bot.send_message(message.chat.id, config.REPLICAS["admin_help"])
            send_group(message)
            bot.register_next_step_handler(message, admin_logic)


def download(message):
    if check_message_type(message):
        try:
            data = list(map(int, message.text[1:].split("_")))
        except Exception as e:
            print(e.args)
            return
        month = data[0]
        year = data[1]
        file = Excel.gaps_on_date_file(month, year)
        bot.send_document(message.chat.id, file)
        send_commands(message)


def mark_users(message):
    if check_message_type(message):
        try:
            global selected
            names = []
            selected = []
            data = list(map(str, message.text.split(" ")))
            def_hours = int(data[0][1:])
            data.pop(0)

            for el in data:
                print(el)

            cur_day = dt.date.today().day
            cur_month = dt.date.today().month
            cur_year = dt.date.today().year

            for el in data:
                hours = 0
                valid = 1
                try:
                    cur_data = list(map(str, el.split('h')))
                    el = cur_data[0]
                    hours = int(cur_data[1])
                    index = el
                    if el[len(el) - 1] == '*':
                        valid = 0
                        index = el[:-1]
                except Exception as e:
                    index = el
                    if el[len(el) - 1] == '*':
                        valid = 0
                        index = el[:-1]
                index = int(index)
                person = group[index - 1]
                PersonModel.mark(person["id"], cur_year, cur_month, cur_day, valid, hours if hours > 0 else def_hours)

            bot.send_message(message.chat.id, "Вы выбрали: ")
            send_selected(message)
            send_commands(message)

        except Exception as e:
            bot.send_message(message.chat.id, config.REPLICAS["some_err"])
            Fun.addToLog(e.args, "ERROR")
            return


def remark_users(message):
    if check_message_type(message):
        PersonModel.delete_marked_on(dt.date.today().day, dt.date.today().month, dt.date.today().year)
        mark_users(message)


def handle_commands(messages):
    for message in messages:
        comm = message.text

        if check_message_type(message):
            if comm == "/start":
                bot.send_message(message.chat.id, "Привет")
                Fun.print_arr(bot, message, config.COMMANDS)

            if comm == "/show_group":
                load_group_res()
                send_group(message)
                send_commands(message)

            elif comm == "/mark":
                send_group(message)
                if len(selected) > 0:
                    bot.send_message(message.chat.id, "Отмеченные:")
                    send_selected(message)
                bot.send_message(message.chat.id, config.REPLICAS["mark"])
                bot.register_next_step_handler(message, mark_users)

            elif comm == "/show_marked":
                if len(selected) == 0:
                    bot.send_message(message.chat.id, "Вы пока никого не выбрали")
                else:
                    send_selected(message)
                send_commands(message)

            elif comm == "/remark":
                send_group(message)
                bot.send_message(message.chat.id, config.REPLICAS["remark"])
                bot.register_next_step_handler(message, remark_users)

            elif comm == "/help":
                send_commands(message)

            elif comm == config.ADMIN["ENTER_COMMAND"]:
                bot.send_message(message.chat.id, "Введите логин и пароль через пробел")
                bot.register_next_step_handler(message, admin_namespace)

            elif comm == "/download":
                dates = PersonModel.get_all_dates()
                if len(dates) == 0:
                    bot.send_message(message.chat.id, "Пока нечего выводить")
                    send_commands(message)
                    continue
                bot.send_message(message.chat.id, "Доступные для вывода: ")
                text = ""
                for date in dates:
                    text += f"/{date['month']}_{date['year']}\n\n"
                bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(message, download)

            else:
                bot.send_message(message.chat.id, config.REPLICAS["command_input_err"])


while True:
    try:
        # try:
        #     file_list = [file for file in os.listdir("cash")]
        #     for file in file_list:
        #         os.remove(os.path.join("cash", file))
        # except OSError as e:
        #     Fun.addToLog(e.args)
        load_group_res()
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.set_update_listener(handle_commands)
        bot.polling()
    except Exception as e:
        print(e.args)
        Fun.addToLog(e.args)
        time.sleep(2)

#
# load_group_res()
# bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()
# bot.set_update_listener(handle_commands)
# bot.polling()

# init()
