import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('___вставить токен бота между ковычками___')

r = requests.get('https://sinoptik.ua/погода-тирасполь')
html = BS(r.content, 'html.parser')
for el in html.select('#content'):
	t_min =el.select('.temperature .min')[0].text
	t_max =el.select('.temperature .max')[0].text
	text = el.select('.wDescription .description')[0].text
	print(t_min + ', ' + t_max + '\n' + text)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(message.chat.id, "Добро пожаловать! Если нужен другой город - напишите его в чат мне. Я сейчас могу подсказать погоду в Тирасполе: \n" + t_min + ', ' + t_max + '\n' + text .format(message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(content_types=['text'])
def pogoda(message):
	user_text = message.text
	res = requests.get('https://sinoptik.ua/погода-' + user_text)
	html = BS(res.content, 'html.parser')
	for el in html.select('#content'):
		t_min =el.select('.temperature .min')[0].text
		t_max =el.select('.temperature .max')[0].text
		text = el.select('.wDescription .description')[0].text
		bot.send_message(message.chat.id, "Сегодня в " + user_text +' '+ t_min + ', ' + t_max + '\n' + text)


bot.polling(none_stop=True)
