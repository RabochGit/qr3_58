import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
from random import randrange

state_storage = StateMemoryStorage()
TOKEN = "6669317935:AAH6y4WQ5eV1bTZBQ93AIrSxeguvypbDU5A"
bot = telebot.TeleBot(token=TOKEN,
                      state_storage=state_storage,
                      parse_mode='Markdown')


class RegState(StatesGroup):
    """
    Класс стейтов регистрации
    """
    fullname = State()
    name = State()
    position = State()


class HelpState(StatesGroup):
    """
        Класс стейта помощи
    """
    get_result = State()


text_start = 'Регистрация!'
text_reg = "Повторная регистрация"
text_button_1 = "Рабочий ноушен"
text_button_2 = "Связь с руководителем"
text_button_3 = "Помощь"

start_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
start_keyboard.add(
    telebot.types.KeyboardButton(
        text_start,
    )
)

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_reg,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Пройдешь регистрацию?',  # Можно менять текст
        reply_markup=start_keyboard)


@bot.message_handler(func=lambda message: text_reg == message.text or text_start == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Принято! Для регистрации введи свою *фамилию*',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, RegState.fullname, message.chat.id)


@bot.message_handler(state=RegState.fullname)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fullname'] = message.text
    bot.send_message(message.chat.id, 'Супер! Теперь мне необходимо узнать Ваше *имя*')
    bot.set_state(message.from_user.id, RegState.name, message.chat.id)


@bot.message_handler(state=RegState.name)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
        bot.send_message(message.chat.id, f'{data["name"]}, необходимо указать Ваш *отдел* '
                                          f'в [Умскул](https://www.umschools.ru/)')
    bot.set_state(message.from_user.id, RegState.position, message.chat.id)


@bot.message_handler(state=RegState.position)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['position'] = message.text
        bot.send_message(message.chat.id, 'Спасибо за регистрацию!\n\n'
                                          f'Ваши данные:\n\n'
                                          f'ФИО: {data["fullname"]} {data["name"]}\n\n'
                                          f'Отдел {data["position"]}', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Держи ссылку на рабочий [Ноушен](https://www.notion.so) "
                                      "твоего отдела", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Твой руководитель: [Рук](https://www.vk.com) ",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Опиши свою проблему одним сообщением",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, HelpState.get_result, message.chat.id)


@bot.message_handler(state=HelpState.get_result)
def age(message):
    bot.send_message(message.chat.id, f'Принято!\n № запроса: `{randrange(10000,90000)}`\n\n'
                                      f'Твой вопрос будет передан. Ожидай ответа',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()