import telebot;
import sqlite3;
from datetime import datetime;
from telebot import types;
bot = telebot.TeleBot('7024265024:AAHZuSAocy8n0YQ5-wBMAbq58hT_PCchvD0')
conn = sqlite3.connect('bd.db', check_same_thread=False)
cursor = conn.cursor()
# Создание таблицы для хранения сообщений, если она еще не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, message TEXT, time DATETIME, robot_type TEXT)''')
conn.commit()
@bot.message_handler(commands=['getdata'])
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Получаем данные о пользователе и сообщении
    user_name = message.from_user.first_name
    text1 = message.text
    fanuc = message.text[:8]
    yask = message.text[:10]
    rlk = message.text[:5]
    gsk = message.text[:5]
    fanuct ='Fanuc'
    yaskt ='Yaskawa'
    gskt = 'GSK'
    rlkt = 'РЛК'
    
    if 'Fanuc 4' in text1 or 'Fanuc 5' in text1 or 'Fanuc 6' in text1 or 'Fanuc 7' in text1 or 'Fanuc 31' in text1:
        time = datetime.now().strftime("%d.%m В %H:%M")
        cursor.execute("INSERT INTO messages (user_name, message, time, robot_type) VALUES (?, ?, ?, ?)", (user_name, text1, time, fanuc))
        conn.commit()
        
        # Отвечаем пользователю
        bot.reply_to(message, "Сообщение сохранено")
    elif 'Yaskawa 40' in text1 or 'Yaskawa 8г' in text1 or 'Yaskawa 1' in text1:
        time = datetime.now().strftime("%d.%m В %H:%M")
        cursor.execute("INSERT INTO messages (user_name, message, time, robot_type) VALUES (?, ?, ?, ?)", (user_name, text1, time, yask))
        conn.commit()
        
        # Отвечаем пользователю
        bot.reply_to(message, "Сообщение сохранено")
    elif 'GSK 1' in text1 or 'GSK 2' in text1:
        time = datetime.now().strftime("%d.%m В %H:%M")
        cursor.execute("INSERT INTO messages (user_name, message, time, robot_type) VALUES (?, ?, ?, ?)", (user_name, text1, time, gsk))
        conn.commit()
        
        # Отвечаем пользователю
        bot.reply_to(message, "Сообщение сохранено")
    elif 'РЛК 2' in text1 or 'РЛК 4' in text1 or 'РЛК 5' in text1:
        time = datetime.now().strftime("%d.%m В %H:%M")
        cursor.execute("INSERT INTO messages (user_name, message, time, robot_type) VALUES (?, ?, ?, ?)", (user_name, text1, time, rlk))
        conn.commit()
        
        # Отвечаем пользователю
        bot.reply_to(message, "Сообщение сохранено")
    elif '/clear' in text1:
        cursor.execute("DELETE FROM messages")
        conn.commit()
        bot.reply_to(message, "Данные в базе данных успешно очищены.")
    elif '/stats' in text1:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = types.KeyboardButton('/ALL')
        button2 = types.KeyboardButton('/FANUC')
        button3 = types.KeyboardButton('/YASKAWA')
        button4 = types.KeyboardButton('/GSK')
        button5 = types.KeyboardButton('/РЛК')
    
        keyboard.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, "Выберите робота:", reply_markup=keyboard)
    elif text1 == '/ALL':
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        # Отправляем пользователю содержимое базы данных
        response = "Содержимое базы данных:\n"
        for row in rows:
            response += f"{row[5]}, {row[4]}: {row[1]}, {row[3]} \n"
        bot.reply_to(message, response)
    elif text1 == '/YASKAWA':
        cursor.execute("SELECT * FROM messages WHERE message LIKE ?", (f'{yaskt}%',))
        rows = cursor.fetchall()
        # Отправляем пользователю содержимое базы данных
        response = "Содержимое базы данных:\n"
        for row in rows:
            response += f"{row[5]}, {row[4]}: {row[1]}, {row[3]} \n"
        bot.reply_to(message, response)
    elif text1 == '/FANUC':
        cursor.execute("SELECT * FROM messages WHERE message LIKE ?", (f'{fanuct}%',))
        rows = cursor.fetchall()
        # Отправляем пользователю содержимое базы данных
        response = "Содержимое базы данных:\n"
        for row in rows:
            response += f"{row[5]}, {row[4]}: {row[1]}, {row[3]} \n"
        bot.reply_to(message, response)
    elif text1 == '/GSK':
        cursor.execute("SELECT * FROM messages WHERE message LIKE ?", (f'{gskt}%',))
        rows = cursor.fetchall()
        # Отправляем пользователю содержимое базы данных
        response = "Содержимое базы данных:\n"
        for row in rows:
            response += f"{row[5]}, {row[4]}: {row[1]}, {row[3]} \n"
        bot.reply_to(message, response)
    elif text1 == '/РЛК':
        cursor.execute("SELECT * FROM messages WHERE message LIKE ?", (f'{rlkt}%',))
        rows = cursor.fetchall()
        # Отправляем пользователю содержимое базы данных
        response = "Содержимое базы данных:\n"
        for row in rows:
            response += f"{row[5]}, {row[4]}: {row[1]}, {row[3]} \n"
        bot.reply_to(message, response)  
    elif '/txt' in text1:
        cursor.execute("SELECT time, message FROM messages")
        data = cursor.fetchall()
        filename = 'Статистика.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            for row in data:
                file.write(str(row) + '\n')
        # Отправка файла пользователю
        with open(filename, 'rb') as file:
            bot.send_document(message.chat.id, file)
    elif '/help' in text1:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = types.KeyboardButton('/stats')
        button2 = types.KeyboardButton('/help')
        button3 = types.KeyboardButton('/txt')
        button4 = types.KeyboardButton('/clear')
        keyboard.add(button1, button2, button3, button4)

    # Отправка клавиатуры с кнопками пользователю
        bot.send_message(message.chat.id, "Доступные команды:", reply_markup=keyboard)
    else:
        # Отвечаем пользователю
        bot.reply_to(message, "Некорректное сообщение !\n\nВведите ошибку, начиная со слов 'Fanuc 4','Fanuc 5','Fanuc 6','Fanuc 7','Fanuc 31','Yaskawa 40', 'Yaskawa 8гр', 'Yaskawa 1', 'GSK 1', 'GSK 2', 'РЛК 2', 'РЛК 4', 'РЛК 5' \n\n/stats - для просмотра статистики \n\n/txt - получить текстовый файл статистики\n\n/clear - очистить статисткику. Пользоваться только при необходимости ! \n\nВ конце месяца, когда выгрузили статистику, используем /clear, что бы очистить статистику и начать сбор новой." )

bot.polling()




