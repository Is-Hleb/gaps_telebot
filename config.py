TOKEN = ""

ADMIN = {
    "PASSWORD": "admin",
    "LOGIN": "admin",
    "ENTER_COMMAND": "/admin"
}


COMMANDS = [
    "/mark - указать отсутствующих",
    "/show_group - вывести группу",
    "/show_marked - вывести отмеченных",
    "/remark - отметить заново",
    "/download - скачать таблицы"
]

REPLICAS = {
    "some_err": "Возникла какая-то ошибка, попробуйте совершить действие повторно",
    "send_welcome": "Привет, введи /help",
    "mark": "В конце имени добавьте *, если причина отсутствия не уважительная",
    "remark": "Введите номера отсутствующих, В конце имени добавьте *, если причина отсутствия не уважительная",
    "admin_help": """Введите либо номера людей, которых вы хотите удалить, либо имена и фамилии тех, котороых хотите
                  добавить через *""",
    "input_err": "Сообщение имеет не верный формат",
    "command_input_err": "Такой команды не существует, введите /help для просмотравозможных команд"
}
