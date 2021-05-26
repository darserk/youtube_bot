from core.database import DataBase


class Ticket:
    def __init__(self, data: dict, db: DataBase = None):
        self.id = data['_id']
        self.date = data['date']
        self.time = data['time']
        self.chat_id = data['chat_id']
        self.status = data['status']
        self.url = data['url']
