import telebot
from buttons import *
from db import conn, cur

with open('config.txt') as cnf:
    API, password, programmer = [i.strip() for i in cnf.readlines()]

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def to_start(message):
    mess_id = message.chat.id
    users_data, teachers_data = get_user_from_db()
    if mess_id in users_data or mess_id in teachers_data:
        bot.send_message(mess_id, f'С возвращением, <b><i>{message.chat.first_name}</i></b>', parse_mode="HTML")
        return_to_main(mess_id)
    else:
        bot.send_message(mess_id, f'Здравствуйте, <b><i>{message.chat.first_name}</i></b>', parse_mode="HTML")
        to_registr(mess_id)

def to_registr(mess_id):
    mess = bot.send_message(mess_id, 'Скажите, кто Вы:', reply_markup=button_start())
    bot.register_next_step_handler(mess, choose_categ)

def return_to_main(mess_id):
    users_data, teachers_data = get_user_from_db()
    all_data = {**users_data, **teachers_data}
    if all_data[mess_id][1] == 'off':
        btn = types.KeyboardButton('Подписаться на рассылку')
    else:
        btn = types.KeyboardButton('Отписаться от рассылки')
    if all_data[mess_id][0] == 'teacher':
        bot.send_message(mess_id, 'Выберите действие:', reply_markup=button_teacher(btn))
    else:
        bot.send_message(mess_id, 'Выберите действие:', reply_markup=button_main(btn))

def choose_categ(message):
    mess_id = message.chat.id
    categ = ['Ученик', 'Родитель', 'Гость', 'Учитель']
    if message.text in categ:
        bot.send_message(mess_id, 'Добро пожаловать!')
        if message.text == categ[0]:
            mes = bot.send_message(mess_id, 'Пожалуйста, скажите: в каком Вы классе. Например, <<5А>>', reply_markup=button_return())
            bot.register_next_step_handler(mes, choose_class, 'student')
        elif message.text == categ[1]:
            mes = bot.send_message(mess_id,'Пожалуйста, скажите: в каком классе обучается Ваш ребёнок. Например, <<5А>>', reply_markup=button_return())
            bot.register_next_step_handler(mes, choose_class, 'parent')
        elif message.text == categ[2]:
            user = (mess_id, 'guest', 'off', message.from_user.first_name, 'none')
            register_in_db(user)
        elif message.text == categ[3]:
            mess = bot.send_message(mess_id, 'Пожалуйста, введите пароль:', reply_markup=button_return())
            bot.register_next_step_handler(mess, input_password)
    else:
        bot.send_message(mess_id, 'Извините, я не понимаю Вас')
        to_registr(mess_id)

def choose_class(message, categ):
    mess_id = message.chat.id
    if message.text != 'Назад':
        class_student = message.text
        user = (mess_id, categ, 'off', message.from_user.first_name, class_student)
        register_in_db(user)
    else:
        to_registr(message.chat.id)

def input_password(message):
    if message.text != 'Назад':
        if message.text == password:
            bot.send_message(message.chat.id, 'Вы успешно вошли')
            mess = bot.send_message(message.chat.id, 'Пожалуйста, скажите свои <b>фамилию</b> и <b>имя </b>. Они будут использоваться при отправке новостей', parse_mode='HTML')
            bot.register_next_step_handler(mess, user_teacher)
        else:
            bot.send_message(message.chat.id, 'Пароль неверный. Повторите попытку')
            mess = bot.send_message(message.chat.id, 'Пожалуйста, введите пароль:')
            bot.register_next_step_handler(mess, input_password)
    else:
        to_registr(message.chat.id)

def user_teacher(message):
    user = (message.chat.id, 'teacher', 'off', message.text, 'none')
    register_in_db(user)

def register_in_db(user):
    try:
        cur.execute("""INSERT OR IGNORE INTO users(user_id, categories, reply, username, form) VALUES(?, ?, ?, ?, ?)""", user)
        conn.commit()
        bot.send_message(user[0], 'Спасибо! Я запомнил')
        return_to_main(user[0])
    except:
        bot.send_message(user[0], 'Извините, возникла ошибка. Сообщите об этом тех. поддержке через кнопку ниже', reply_markup=button_to_support())

def get_user_from_db():
    cur.execute("""SELECT user_id, categories, reply, username, form FROM users""")
    users_data, teachers_data = {}, {}
    for i in cur.fetchall():
        user_id = i[0]
        if i[1] == 'teacher':
            teachers_data[user_id] = i[1::]
        else:
            users_data[user_id] = i[1::]
    return users_data, teachers_data

@bot.message_handler(func=lambda message: message.text == 'Подписаться на рассылку')
def reply_on(message):
    mess_id = message.chat.id
    try:
        cur.execute("""UPDATE users set reply = ? where user_id = ?""", ('on', message.chat.id))
        conn.commit()
        bot.send_message(mess_id, 'Вы успешно подписались на рассылку')
        return_to_main(mess_id)
    except:
        bot.send_message(mess_id, 'Возникла ошибка')
        return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Отписаться от рассылки')
def reply_off(message):
    mess_id = message.chat.id
    try:
        cur.execute("""UPDATE users set reply = ? where user_id = ?""", ('off', message.chat.id))
        conn.commit()
        bot.send_message(mess_id, 'Вы успешно отписались от рассылки')
        return_to_main(mess_id)
    except:
        bot.send_message(mess_id, 'Возникла ошибка')
        return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Связь с поддержкой')
def to_support(message):
    mess = bot.send_message(message.chat.id, 'Введите сообщение:', reply_markup=button_return())
    bot.register_next_step_handler(mess, send_to_support)

def send_to_support(message):
    mess_id = message.chat.id
    if message.text != 'Назад':
        bot.forward_message(programmer, message.chat.id, message.message_id)
        bot.send_message(mess_id, 'Сообщение успешно отправлено.')
        return_to_main(mess_id)
    else:
        return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Отправить сообщение')
def send_mess(message):
    users_data, teachers_data = get_user_from_db();
    mess_id = message.chat.id
    if mess_id in teachers_data:
        mess = bot.send_message(message.chat.id, 'Выберите, кому Вы хотите отправить новость:', reply_markup=button_to_whom_reply())
        bot.register_next_step_handler(mess, to_whom)

def to_whom(message):
    mess_id = message.chat.id
    text = message.text
    if text != 'Назад':
        if text == 'Ученикам' or text == 'Родителям':
            if text == 'Ученикам':
                send_user = ['student']
            else:
                send_user = ['parent']
            mess = bot.send_message(mess_id,'Напишите нужный класс. Пожалуйста, пишите номер и букву класса <b>слитно</b> (Например, <i>5А</i>)', reply_markup=button_return(), parse_mode='HTML')
            bot.register_next_step_handler(mess, get_form, send_user)
        elif text == 'Гостям' or text == 'Учителям':
            if text == 'Гостям':
                send_user = ['guest', 'all']
            else:
                send_user = ['teacher', 'all']
            choose_type_mess(message, send_user)
        elif text == 'Всем...':
            mess = bot.send_message(message.chat.id, 'Выберите, кому Вы хотите отправить новость:', reply_markup=button_who_all())
            bot.register_next_step_handler(mess, category_all)
        else:
            print(text)
            bot.send_message(message.chat.id, 'Извините, я не понимаю Вас')
            return_to_main(mess_id)
    else:
        return_to_main(mess_id)

def get_form(message, send_users):
    send_users.append(message.text)
    choose_type_mess(message, send_users)

def category_all(message):
    if message.text != 'Назад':
        if message.text == '...Родителям':
            send_user = ['parent', 'all']
        elif message.text == '...Ученикам':
            send_user = ['student', 'all']
        elif message.text == 'Всем':
            send_user = ['all', 'all']
        else:
            bot.send_message(message.chat.id, 'Извините, я не понимаю Вас')
            return_to_main(message.chat.id)
        choose_type_mess(message, send_user)
    else:
        return_to_main(message.chat.id)

def choose_type_mess(message, send_user):
    if message.text != 'Назад':
        mess = bot.send_message(message.chat.id, 'Пожалуйста, выберите тип сообщения (в каждом можно использовать текст). На компьютере, при отправки любого типа, кроме текста, нужно выбрать файл', reply_markup=button_type_message())
        bot.register_next_step_handler(mess, get_type_mess, send_user)
    else:
        return_to_main(message.chat.id)

def get_type_mess(message, send_user):
    if message.text != 'Назад':
        if message.text == 'Только текст':
            type_message = 'text'
            mess = bot.send_message(message.chat.id, "Пожалуйста, введите его:", reply_markup=button_return())
            bot.register_next_step_handler(mess, choose_user_by_bot, send_user, type_message)
        else:
            if message.text == 'Фото':
                type_message = 'photo'
            elif message.text == 'Видео':
                type_message = 'video'
            elif message.text == 'Файл':
                type_message = 'file'
            else:
                bot.send_message(message.chat.id, 'Извините, я не понимаю Вас')
                return_to_main(message.chat.id)
            mess = bot.send_message(message.chat.id, "Пожалуйста, прикрепите его:", reply_markup=button_return())
            bot.register_next_step_handler(mess, choose_user_by_bot, send_user, type_message)
    else:
        return_to_main(message.chat.id)

def set_caption(message, teacher_name):
    try:
        return f'<i><b>{teacher_name}</b></i>: \n' + message.caption
    except:
        return f'<i><b>{teacher_name}</b></i>:'

def choose_type_by_bot(message, type_message, list_users, teacher_name):
    text = set_caption(message, teacher_name)
    for user_id in list_users:
        bot.send_message(user_id, f'Здравствуйте, {list_users[user_id]}. Доступно новое сообщение')
        if type_message == 'text':
            send_text(message, user_id, teacher_name)
        elif type_message == 'photo':
            send_photo(message, user_id, text)
        elif type_message == 'video':
            send_video(message, user_id, text)
        elif type_message == 'file':
            send_file(message, user_id, text)

def send_text(message, userid, teacher_name):
    news = message.text
    bot.send_message(userid, f'<i><b>{teacher_name}</b></i>: \n' + news, parse_mode='HTML')

def send_photo(message, userid, text):
    photo_id = message.photo[0].file_id
    bot.send_photo(userid, photo_id, caption=text, parse_mode='HTML')

def send_video(message, userid, text):
    video_id = message.video.file_id
    bot.send_video(userid, video_id, caption=text, parse_mode='HTML')

def send_file(message, userid, text):
    file_id = message.document.file_id
    bot.send_document(userid, file_id, caption=text, parse_mode='HTML')

def choose_user_by_bot(message, send_user, type_message):
    mess_id = message.chat.id
    if message.text != 'Назад':
        users_data, teachers_data = get_user_from_db()
        all_data = {**users_data, **teachers_data}
        teacher_name = teachers_data[mess_id][2]
        list_user_to_send = {}
        try:
            for u_id in all_data:
                if all_data[u_id][1] == 'on' and send_user[0] == 'all' and send_user[1] == 'all':
                    list_user_to_send[u_id] = all_data[u_id][2]
                elif send_user[0] == all_data[u_id][0] and (send_user[1] == all_data[u_id][3] or send_user[1] == 'all'):
                    list_user_to_send[u_id] = all_data[u_id][2]
            choose_type_by_bot(message, type_message, list_user_to_send, teacher_name)
            bot.send_message(message.chat.id, 'Сообщение успешно отправлено')
            return_to_main(mess_id)
        except:
            bot.send_message(message.chat.id, 'Возникла ошибка. Пожалуйста, сообщите об этом разработчику', reply_markup=button_to_support())

    else:
        return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Изменить расписание')
def type_schedule(message):
    mess_id = message.chat.id
    _, teachers_data = get_user_from_db()
    if mess_id in teachers_data:
        mess = bot.send_message(mess_id, 'Выберите, какое расписание Вы хотите изменить', reply_markup=button_type_schedule())
        bot.register_next_step_handler(mess, to_change_schedule)

def to_change_schedule(message):
    mess_id = message.chat.id
    if message.text != 'Назад':
        if message.text == 'Основное':
            type_sch = 'main'
        elif message.text == 'Временное':
            type_sch = 'temp'
        else:
            bot.send_message(mess_id, 'Извините, я не понимаю Вас')
            return_to_main(mess_id)
        mess = bot.send_message(message.chat.id, 'Пожалуйста, прикрепите фото (<i>на компьютере необходимо выбрать <b>Сжать изображение</b>)</i>', reply_markup=button_return(), parse_mode='HTML')
        bot.register_next_step_handler(mess, save_schedule, type_sch)
    else:
        return_to_main(mess_id)

def save_schedule(message, type_sch):
    mess_id = message.chat.id
    if message.text != 'Назад':
        try:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'schedule_{type_sch}.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(mess_id, 'Расписание успешно изменено')
            message.text = 'Расписание было обновлено'
            choose_user_by_bot(message, ['all', 'all'], 'text')
        except Exception:
            bot.send_message(mess_id, 'Произошла ошибка. Свяжитесь с поддержкой', reply_markup=button_to_support())
    else:
        return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Узнать расписание')
def choose_type_Schedule(message):
    mess = bot.send_message(message.chat.id, 'Выберите, какое расписание Вы хотите узнать:', reply_markup=button_type_schedule())
    bot.register_next_step_handler(mess, get_schedule)

def get_schedule(message):
    mess_id = message.chat.id
    if message.text != 'Назад':
        if message.text == 'Основное':
            with open('schedule_main.jpg', 'rb') as schedule:
                bot.send_photo(mess_id, schedule)
        elif message.text == 'Временное':
            with open('schedule_temp.jpg', 'rb') as schedule:
                bot.send_photo(mess_id, schedule)
        else:
            bot.send_message(message.chat.id, 'Извините, я не понимаю Вас')
    return_to_main(mess_id)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def ret(message):
    return_to_main(message.chat.id)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print(Exception)
