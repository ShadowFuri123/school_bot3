from telebot import types

def button_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Гость')
    btn2 = types.KeyboardButton('Ученик')
    btn3 = types.KeyboardButton('Учитель')
    btn4 = types.KeyboardButton('Родитель')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def button_main(btn1):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('Узнать расписание')
    btn3 = types.KeyboardButton('Связь с поддержкой')
    markup.add(btn1, btn2, btn3)
    return markup


def button_teacher(btn4):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отправить сообщение')
    btn2 = types.KeyboardButton('Изменить расписание')
    btn3 = types.KeyboardButton('Узнать расписание')
    btn5 = types.KeyboardButton('Связь с поддержкой')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def button_return():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    markup.add(btn1)
    return markup

def button_to_whom_reply():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Гостям')
    btn2 = types.KeyboardButton('Ученикам')
    btn3 = types.KeyboardButton('Учителям')
    btn4 = types.KeyboardButton('Родителям')
    btn5 = types.KeyboardButton('Всем...')
    btn6 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


def button_who_all():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Всем')
    btn2 = types.KeyboardButton('...Родителям')
    btn3 = types.KeyboardButton('...Ученикам')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def button_type_message():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Только текст')
    btn2 = types.KeyboardButton('Фото')
    btn3 = types.KeyboardButton('Видео')
    btn4 = types.KeyboardButton('Файл')
    btn5 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def button_type_schedule():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Основное')
    btn2 = types.KeyboardButton('Временное')
    btn3 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3)
    return markup

def button_to_support():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Связь с поддержкой')
    return markup
