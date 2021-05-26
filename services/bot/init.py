import telebot
import re
from core.config import TELEGRAM_TOKEN, REGEXP_YOUTUBE
from core.mood import Mood
from core.tickets import Tickets

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Укажи полную ссылку на видео в youtube, "
                                      "чтобы я смог проанализировать тональность комментариев")


# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.send_message(message.chat.id, "Готов помочь")


@bot.message_handler(regexp=REGEXP_YOUTUBE)
def analyze(message):
    result = Tickets.add(message.chat.id, message.text)
    if result:
        message_txt = "Ваша заявка на анализ комментариев зарегистрирована. Ожидайте ответа... :("
    else:
        message_txt = "Ваша заявка не зарегистрирована. Попробуйте позже."
    bot.send_message(message.chat.id, message_txt)


@bot.message_handler(func=lambda m: True)
def check_url(message):
    bot.send_message(message.chat.id, "Укажите ссылку на видео в ютубе.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
