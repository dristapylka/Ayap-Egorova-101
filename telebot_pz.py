import telebot
import random
from telebot import types
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

API_TOKEN = '7682166859:AAEk-6L1RbdO1XLBgEEc069TVZya1Is4gRc'
bot = telebot.TeleBot(API_TOKEN)


STICKER_IDS = [
    "CAACAgIAAxkBAAEOe1BoA2p4JLLJyViaNtp3rccj1N9p5wACPCEAAtwlkEpM0i5LdMCGfDYE",
    "CAACAgIAAxkBAAEOe1JoA2qRMbjwd1uzygHVinuQDuQwRAACOigAAlMokUrrUvFF9JBAZTYE",
    "CAACAgIAAxkBAAEOe1RoA2rB3iUHc1DsIeb4V3sXWm050AACUg8AAhA1yUlhGR6piIKYRTYE",
	"CAACAgIAAxkBAAEOe1ZoA2r4wM9_O8etfmmYj5v8WgScBwAC2mgAAmfCCUrdXSgUvCrz7DYE"
]



# Handle '/start' and '/help'
@bot.message_handler(commands=['buttons', 'start'])
def send_welcome(message):
	markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
	button1=types.KeyboardButton("Привет")
	button2=types.KeyboardButton("Узнать погоду")
	button_s=types.KeyboardButton("Получить стикер")
	button_g=types.KeyboardButton("Получить график")
	markup.add(button1, button2,button_s,button_g)
	bot.send_message(message.chat.id,'Ты обращаешься ко мне но делаешь это без уважения', reply_markup=markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
	if message.text == "Привет":
		bot.reply_to(message, message.text+" человек")
	elif message.text == "Узнать погоду":
		markup = types.InlineKeyboardMarkup()
		button3 = types.InlineKeyboardButton("Москва", callback_data='get_weatherM')
		button4 = types.InlineKeyboardButton("Питер", callback_data='get_weatherP')
		markup.add(button3)
		markup.add(button4)
		bot.send_message(message.chat.id, "Выбери город".format(message.from_user.first_name), reply_markup=markup)
	elif message.text == "Получить стикер":
		random_sticker = random.choice(STICKER_IDS)
		bot.send_sticker(message.chat.id, random_sticker)
		#bot.reply_to(message, '', callback_data='sticker')
	elif message.text == "Получить график":
		markup = types.InlineKeyboardMarkup()
		button_k = types.InlineKeyboardButton("Ввести коэффициенты", callback_data='graph')
		markup.add(button_k)
		bot.send_message(message.chat.id, "Сейчас вам предстоит ввести коэффициенты для задания графика".format(message.from_user.first_name), reply_markup=markup)
	else:
		bot.reply_to(message, message.text)



@bot.callback_query_handler(func=lambda call: call.data == 'get_weatherM')
def get_weatherM(call):
    url = "https://api.openweathermap.org/data/2.5/weather?lat=61.9092&lon=42.6474&appid=e9938fb4f28c49a0a44ec92c44adc703&units=metric&lang=ru"
    response = requests.get(url)
    data = json.loads(response.text)

    if data.get('main'):
        current_temp = data['main']['temp']
        bot.send_message(call.message.chat.id, f"Текущая температура в Москве: {current_temp}°C")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'get_weatherP')
def get_weatherP(call):
    url = "https://api.openweathermap.org/data/2.5/weather?lat=62.9092&lon=43.6474&appid=e9938fb4f28c49a0a44ec92c44adc703&units=metric&lang=ru"
    response = requests.get(url)
    data = json.loads(response.text)

    if data.get('main'):
        current_temp = data['main']['temp']
        bot.send_message(call.message.chat.id, f"Текущая температура в Питере: {current_temp}°C")
    bot.answer_callback_query(call.id)



@bot.callback_query_handler(func=lambda call: call.data == 'sticker')
def sticker(call):
    random_sticker = random.choice(STICKER_IDS)
    bot.send_sticker(call.message.chat.id, random_sticker)
    bot.answer_callback_query(call.id)



@bot.callback_query_handler(func=lambda call: call.data == 'graph')
def graph(call):
    bot.send_message(call.message.chat.id, "Введите коэффициент k1:")
    bot.register_next_step_handler(call.message, get_k1)

def get_k1(message):
    global k1
    try:
        k1 = float(message.text)
        bot.send_message(message.chat.id, "Введите коэффициент k2:")
        bot.register_next_step_handler(message, get_k2)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_k1)

def get_k2(message):
    global k2
    try:
        k2 = float(message.text)
        bot.send_message(message.chat.id, "Введите коэффициент k3:")
        bot.register_next_step_handler(message, get_k3)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_k2)

def get_k3(message):
    global k3
    try:
        k3 = float(message.text)
        draw_graph(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_k3)

def draw_graph(chat_id):
    global k1, k2, k3
    x = np.linspace(0, 100, 400)
    y = k1 * x**2 + k2 * x + k3
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"График y = {k1}*x^2 + {k2}*x + {k3}")
    plt.grid(True)
    plt.savefig("graph.png")
    plt.close()

    with open("graph.png", 'rb') as photo:
        bot.send_photo(chat_id, photo)

bot.infinity_polling()




