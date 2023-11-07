import telebot

user_data = {}

stress_list = list("А́")

# main bot API: 6618183019:AAE71Te6iBwBKRbhmYYGsaC5gz23Ub-gNvg
# test bot API: 6206944614:AAFkdta9HiBznxmXJ8DHb1HbEC5OISByCeU
API_TOKEN = "6206944614:AAFkdta9HiBznxmXJ8DHb1HbEC5OISByCeU"
bot = telebot.TeleBot(API_TOKEN)
stored_massages = {"help_message": "Я – бот для редагування тексту. \nМій функціонал потроху стає все більшим, "
                                   "і нижче ти можеш ознайомитися з командами, які його викликають. \n\n"
                                   "Якщо я не відповідаю – спробуй ввести \n/set_defaults\n\n"
                                   "Команди:\n"
                                   "/info – перегляд сепаратора та символів для видалення\n"
                                   "/separator – зміна сепаратора\n"
                                   "/symbols_to_remove – зміна символів для видалення\n"
                                   "/do_lower_case – чи я понижаю регістр слів\n\n"
                                   "/do_nicer – форматування тексту\n"
                                   "/compare_bunches – попарне співставлення слів з двох груп"}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    set_def(user_id)
    bot.send_message(user_id, f"Привіт! Я бот-редактор Кульбаба!\n\n"
                              f"/separator за замовчуванням: {user_data[user_id]['separator']}\n"
                              f"/symbols_to_remove за замовчуванням: "
                              f"{''.join(user_data[user_id]['symbols_to_remove'])}\n"
                              f"/do_lower_case за замовчуванням: {user_data[user_id]['do_lower_case']}\n\n"
                              f"Якщо все підходить – вводи /do_nicer, і я відформатую все що треба!\n\n"
                              f"А якщо є купа слів, поряд з якими треба написати іншу купу слів – вводи "
                              f"/compare_bunches і я допоможу!")


def set_def(user_id):
    user_data[user_id] = {}
    user_data[user_id]['separator'] = '–'
    user_data[user_id]['symbols_to_remove'] = ['(', ')', '“', '”', '"', '/']
    user_data[user_id]['do_lower_case'] = False
    user_data[user_id]['translation_pairs'] = []
    user_data[user_id]['compared_bunches'] = []


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


@bot.message_handler(commands=['give_my_id'])
def give_my_id(message):
    user_id = message.chat.id
    bot.send_message(user_id, f"your id is {user_id}")
    print(f"user_id: {user_id}")


def set_help_message(message):
    stored_massages['help_message'] = message.text
    bot.send_message(message.chat.id, "Я змінив /help, але не забудь додати нову фразу в код")


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.chat.id
    if user_id not in user_data:
        set_def(user_id)
    bot.send_message(user_id, f"/separator: {user_data[user_id]['separator']}\n"
                              f"/symbols_to_remove: {''.join(user_data[user_id]['symbols_to_remove'])}\n"
                              f"/do_lower_case: {user_data[user_id]['do_lower_case']}\n")


@bot.message_handler(commands=['separator'])
def change_separator(message):
    bot.send_message(message.chat.id, "Введи новий сепаратор")
    bot.register_next_step_handler(message, set_separator)


def set_separator(message):
    user_data[message.chat.id]['separator'] = message.text
    bot.send_message(message.chat.id, f"Чудово, \"{user_data[message.chat.id]['separator']}\" буде "
                                      f"використовуватися як сепаратор")


@bot.message_handler(commands=['symbols_to_remove'])
def change_symbols_to_remove(message):
    bot.send_message(message.chat.id, "Напиши без пробілів які символи ти хочеш щоб я прибирав?")
    bot.register_next_step_handler(message, set_symbols_to_remove)


def set_symbols_to_remove(message):
    user_id = message.chat.id
    user_data[user_id]['symbols_to_remove'] = list(message.text)
    bot.send_message(user_id, f"Ці символи я буду прибирати з тексту: {''.join(user_data[user_id]['symbols_to_remove'])}")


@bot.message_handler(commands=['do_lower_case'])
def change_lower_state(message):
    user_id = message.chat.id
    user_data[user_id]['do_lower_case'] = not user_data[user_id]['do_lower_case']
    bot.send_message(user_id, f"Значення змінене на {user_data[user_id]['do_lower_case']}")


@bot.message_handler(commands=['do_nicer'])
def give_me_text(message):
    bot.send_message(message.chat.id, "Що я маю відформатувати?")
    bot.register_next_step_handler(message, nice_order)


def nice_order(message):
    user_id = message.chat.id
    if user_id not in user_data:
        set_def(user_id)
    if message.text.find(user_data[user_id]["separator"]) == -1:
        bot.send_message(user_id, "Не бачу сепаратора, обробляю як звичайний текст")

    bald_to_pairs(message)
    do_nicer(message)
    nice_out(message)


def bald_to_pairs(message):
    user_id = message.chat.id
    if len(user_data[user_id]['translation_pairs']):
        user_data[user_id]['translation_pairs'].clear()
    separator = user_data[user_id]['separator']
    for sentence in message.text.split('\n'):
        sep_pos = sentence.find(separator)
        if sentence == '':
            pass
        elif sep_pos == -1:
            # if it`s a text - we don`t split it
            user_data[user_id]['translation_pairs'].append(sentence)
        else:
            # here we deside how to split the sentence
            splitter = ""
            if sentence[sep_pos - 1] == ' ':
                splitter += ' '
            splitter += separator
            if sentence[sep_pos + 1] == ' ':
                splitter += ' '

            # to lower or not to lower, that is the question
            if user_data[user_id]['do_lower_case']:
                sentence = sentence.lower()

            user_data[user_id]['translation_pairs'].append(sentence.split(f"{splitter}"))


def do_nicer(message):
    user_id = message.chat.id
    bad_list = user_data[user_id]['symbols_to_remove'] + list(stress_list[1])
    # we are going along the list, doing it nicer
    for i in range(len(user_data[user_id]['translation_pairs'])):
        # there are can be strings and lists in the main list
        string_or_list = user_data[user_id]['translation_pairs'][i]
        if type(string_or_list) == str:
            user_data[user_id]['translation_pairs'][i] = nice_formatting(string_or_list, bad_list)
        else:
            for k in range(len(string_or_list)):
                user_data[user_id]['translation_pairs'][i][k] = nice_formatting(string_or_list[k], bad_list)


def nice_formatting(some_string, bad_list):
    if len(some_string) > 0:
        some_string = remove_wrong(some_string, bad_list)
        last_symbol = some_string[-1]
        if last_symbol == '?' or last_symbol == '!' or last_symbol == '.':
            some_string = some_string.capitalize()
            # here we delete extra spaces
            while some_string.find(f" {last_symbol}") != -1:
                some_string = remove_wrong(some_string, [f" {last_symbol}"], last_symbol)
    return some_string


def remove_wrong(some_string, list_of_wrong_symbols, replace_with=None):
    if replace_with is None:
        replace_with = ''
    for symbol in list_of_wrong_symbols:
        some_string = some_string.replace(symbol, replace_with)
    return some_string


def nice_out(message):
    user_id = message.chat.id
    out_message = ""
    for item in user_data[user_id]['translation_pairs']:
        if type(item) == str:
            out_message += item + '\n'
        else:
            out_message += f"{item[0]} – {item[1]}" + '\n'
    bot.send_message(user_id, out_message)
    print(out_message)


@bot.message_handler(commands=['compare_bunches'])
def do_compare_bunches(message):
    user_id = message.chat.id
    if user_id not in user_data:
        set_def(user_id)
    user_data[user_id]['compared_bunches'] = []
    bot.send_message(user_id, "Відправ перелік слів, що мають стояти ЗЛІВА, не забудь розділити їх ентерами")
    bot.register_next_step_handler(message, take_bunches)


def take_bunches(message):
    user_id = message.chat.id
    user_data[user_id]['compared_bunches'].append(message.text.lower().split('\n'))
    if len(user_data[user_id]['compared_bunches']) < 2:
        bot.send_message(user_id, "Відправ перелік слів, що мають стояти ЗПРАВА, не забудь розділити їх ентерами")
        bot.register_next_step_handler(message, take_bunches)
    else:
        send_compared_bunches(message)


def send_compared_bunches(message):
    user_id = message.chat.id
    out_message = ""
    flen = len(user_data[user_id]['compared_bunches'][0])
    slen = len(user_data[user_id]['compared_bunches'][1])
    if flen != slen:
        bot.send_message(user_id, "Неоднакова кількість слів, не можу їх попарно співставити")
    else:
        for i in range(flen):
            out_message += f"{user_data[user_id]['compared_bunches'][0][i]} – {user_data[user_id]['compared_bunches'][1][i]}" + '\n'
        bot.send_message(user_id, out_message)
        print(out_message)


@bot.message_handler(commands=['compare_sentence_and_bunch'])
def do_compare_sentence_and_bunch(message):
    user_id = message.chat.id
    if user_id not in user_data:
        set_def(user_id)
    user_data[user_id]['compared_bunches'] = []
    bot.send_message(user_id, "Відправ речення, що буде стояти ЗЛІВА, я його продублюю перед усіма словами\n"
                              "Після цього речення я поставлю пробіл, і лише потім додам "
                              "слово з тієї купки, що ти скинеш")
    bot.register_next_step_handler(message, take_sentence)


def take_sentence(message):
    user_id = message.chat.id
    # to lower or not to lower, that is the question
    if user_data[user_id]['do_lower_case']:
        sentence = message.text.lower()
    else:
        sentence = message.text
    user_data[user_id]['compared_bunches'].append(sentence)
    bot.send_message(user_id, "Відправ перелік слів, що мають стояти ЗПРАВА, не забудь розділити їх ентерами")
    bot.register_next_step_handler(message, send_compared_s_and_b)


def send_compared_s_and_b(message):
    user_id = message.chat.id
    out_message = ""
    if user_data[user_id]['do_lower_case']:
        sentence = message.text.lower()
    else:
        sentence = message.text
    user_data[user_id]['compared_bunches'].append(sentence.split('\n'))

    for i in range(len(user_data[user_id]['compared_bunches'][1])):
        out_message += f"{user_data[user_id]['compared_bunches'][0]} {user_data[user_id]['compared_bunches'][1][i]}" + '\n'
    bot.send_message(user_id, out_message)
    print(out_message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(message.text)
    bot.reply_to(message, "*Для форматування введи команду /do_nicer*", parse_mode="Markdown")


@bot.edited_message_handler(func=lambda message: True)
def response_to_edited(message):
    bot.reply_to(message, "Ти ж не думаєш, що я побачу зміни?")


bot.infinity_polling(1)
