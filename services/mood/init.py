from core.tickets import Tickets
from core.database import DataBase
from core.mood import Mood
import telebot
from core.config import TELEGRAM_TOKEN, TIMEOUT_MOOD
from time import sleep


bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


def execute():
    db = DataBase()
    for ticket in Tickets.not_active(db):
        graphic = Mood.analyze(ticket.url)
        bot.send_photo(ticket.chat_id, graphic)
        Tickets.execute(ticket, db)


if __name__ == "__main__":
    while True:
        execute()
        sleep(TIMEOUT_MOOD)




