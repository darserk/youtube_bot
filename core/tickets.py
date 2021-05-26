from core.database import DataBase
from core.ticket import Ticket
import datetime


class Tickets:
    @staticmethod
    def not_active(db: DataBase = None):
        db = db if db is not None else DataBase()
        tickets = db.select('mood', {'status': False})
        tickets = [Ticket(d, db) for d in tickets]
        return tickets

    @staticmethod
    def execute(ticket: Ticket, db: DataBase = None):
        db = db if db is not None else DataBase()
        data = {'status': True}
        where = {'chat_id': ticket.chat_id, 'url': ticket.url, 'status': False}
        request = db.update('mood', data, where)
        return request

    @staticmethod
    def add (chat_id: str, url: str, db: DataBase = None):
        db = db if db is not None else DataBase()
        data = {
            'date': datetime.datetime.now().strftime('%d-%m-%Y'),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'chat_id': chat_id,
            'status': False,
            'url': url
        }
        request = db.insert('mood', data)
        return request
