import telebot

user_data = {}

stress_list = list("А́")

API_TOKEN = "6618183019:AAE71Te6iBwBKRbhmYYGsaC5gz23Ub-gNvg"
bot = telebot.TeleBot(API_TOKEN)
stored_massages = {"help_message": "Я – бот для редагування тексту. \nМоя основна задача – "
                                   "редагування перекладів по типу \n\"двері – door\". \n\n"
                                   "Якщо я не відповідаю – спробуй ввести \n/set_defaults\n\n"
                                   "Команди:\n"
                                   "/info – перегляд сепаратора та символів для видалення\n"
                                   "/separator – зміна сепаратора\n"
                                   "/symbols_to_remove – зміна символів для видалення\n\n"
                                   "/do_nicer – форматування тексту"}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    set_defaults(user_id)
    bot.send_message(user_id, f"Привіт! Я бот-редактор Кульбаба!\n\n"
                              f"/separator за замовчуванням: {user_data[user_id]['separator']}\n"
                              f"/symbols_to_remove за замовчуванням: "
                              f"{''.join(user_data[user_id]['symbols_to_remove'])}\n\n"
                              f"Якщо все підходить – вводи /do_nicer, і я відформатую все що треба")


def set_def(user_id):
    user_data[user_id] = {}
    user_data[user_id]['separator'] = '–'
    user_data[user_id]['symbols_to_remove'] = ['(', ')', '“', '”']
    user_data[user_id]['translation_pairs'] = []


@bot.message_handler(commands=['set_defaults'])
def set_defaults(message):
    user_id = message.chat.id
    set_def(user_id)
    bot.send_message(user_id, "Виставлені значення за замовчанням")


@bot.message_handler(commands=['help'])
def help_mes(message):
    bot.send_message(message.chat.id, stored_massages['help_message'])


@bot.message_handler(commands=['change_help_message_kb_only'])
def change_help_message(message):
    bot.send_message(message.chat.id, stored_massages['help_message'])
    bot.register_next_step_handler(message, set_help_message)


def set_help_message(message):
    stored_massages['help_message'] = message.text
    bot.send_message(message.chat.id, "Я змінив /help, але не забудь додати нову фразу в код")


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, f"/separator: {user_data[message.chat.id]['separator']}\n"
                                      f"/symbols_to_remove: "
                                      f"{''.join(user_data[message.chat.id]['symbols_to_remove'])}\n\n")


@bot.message_handler(commands=['separator'])
def change_separator(message):
    bot.send_message(message.chat.id, "Введи новий сепаратор")
    bot.register_next_step_handler(message, set_separator)


def set_separator(message):
    user_data[message.chat.id]['separator'] = message.text
    bot.send_message(message.chat.id, f"Чудово, \"{user_data[message.chat.id]['separator']}\" буде "
                                      f"використовуватися як сепаратор")


@bot.message_handler(commands=['symbols_to_remove'])
def change_separator(message):
    bot.send_message(message.chat.id, "Напиши без пробілів які символи ти хочеш щоб я прибирав?")
    bot.register_next_step_handler(message, set_symbols_to_remove)


def set_symbols_to_remove(message):
    user_data[message.chat.id]['symbols_to_remove'] = list(message.text)
    bot.send_message(message.chat.id, f"Ці символи я буду прибирати з тексту: "
                                      f"\"{user_data[message.chat.id]['symbols_to_remove']}\" ")


@bot.message_handler(commands=['do_nicer'])
def give_me_text(message):
    bot.send_message(message.chat.id, "Що я маю відформатувати?")
    bot.register_next_step_handler(message, nice_order)
    user_data[message.chat.id]['translation_pairs'].clear()


def nice_order(message):
    bald_to_pairs(message)
    do_nicer(message)
    nice_out(message)


def bald_to_pairs(message):
    user_id = message.chat.id
    print(user_data[user_id]['separator'])
    separator = user_data[user_id]['separator']
    user_data[user_id]['translation_pairs'].clear()
    for item in message.text.split('\n'):
        if item == '':
            pass
        elif item.find(separator) == -1:
            user_data[user_id]['translation_pairs'].append(item.split())
        else:
            user_data[user_id]['translation_pairs'].append(item.split(f" {separator} "))


def remove_wrong(some_string, list_of_wrong_symbols):
    for symbol in list_of_wrong_symbols:
        while 1:
            remove_index = some_string.find(symbol)
            if remove_index != -1:
                some_string = some_string[:remove_index] + some_string[remove_index + 1:]
            else:
                break
    return some_string


def do_nicer(message):
    user_id = message.chat.id
    bad_list = user_data[user_id]['symbols_to_remove']
    for i in range(len(user_data[user_id]['translation_pairs'])):
        for k in range(len(user_data[user_id]['translation_pairs'][i])):
            user_data[user_id]['translation_pairs'][i][k] = remove_wrong(user_data[user_id]['translation_pairs'][i][k],
                                                                         bad_list)
            user_data[user_id]['translation_pairs'][i][k] = remove_wrong(user_data[user_id]['translation_pairs'][i][k],
                                                                         stress_list[1])


def nice_out(message):
    out_message = ""
    for item in user_data[message.chat.id]['translation_pairs']:
        out_message += f"{item[0]} – {item[1]}" + '\n'
    bot.send_message(message.chat.id, out_message)
    print(out_message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(message.text)
    bot.reply_to(message, "Для форматування введи команду /do_nicer")


bot.infinity_polling(1)
