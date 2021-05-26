from ssl import CERT_NONE
from core.config import MONGO_DB, MONGO_LOGIN, MONGO_PASSWORD, MONGO_CONNECTION_URL
from pymongo import MongoClient


class DataBase:
    __instance = None

    # singleton
    @staticmethod
    def instance(collection: str):
        if DataBase.__instance is None:
            DataBase()
        return DataBase.__instance[collection]

    def __init__(self):
        if DataBase.__instance is None:
            self.__connection_url = MONGO_CONNECTION_URL.format(
                MONGO_LOGIN,
                MONGO_PASSWORD,
                MONGO_DB
            )
            DataBase.__instance = MongoClient(self.__connection_url, ssl=True, ssl_cert_reqs=CERT_NONE)
            DataBase.__instance = DataBase.__instance[MONGO_DB]

    # выборка данных
    def select(self, collection_name: str, where: dict = {}):
        collection = DataBase.instance(collection_name)
        response = collection.find(where)
        result = list(response)
        return result

    def aggregate(self, collection_name: str, lookup: dict, where: dict = {}):
        collection = DataBase.instance(collection_name)
        response = collection.aggregate([{'$lookup': lookup}, {'$match': where}])
        result = list(response)
        return result

    # проверка на существование элемента
    def exist(self, collection_name: str, where: dict = {}):
        collection = DataBase.instance(collection_name)
        if not collection.count_documents(where):
            return False
        return True

    # вставка данных
    def insert(self, collection_name: str, data, where: dict = {}):
        collection = DataBase.instance(collection_name)
        if self.exist(collection_name, where) and len(where):
            return False
        return collection.insert_one(data).inserted_id

    # вставка большого количества данных
    def insert_many(self, collection_name: str, data, where: dict = {}):
        collection = DataBase.instance(collection_name)
        if self.exist(collection_name, where) and len(where):
            return False
        return collection.insert_many(data).inserted_id

    # обновление данных
    def update(self, collection_name: str, data: dict = {}, where: dict = {}):
        collection = DataBase.instance(collection_name)
        return collection.update_one(where, {'$set': data}).modified_count

    # удаление данных
    def delete(self, collection_name: str, where: dict = {}):
        collection = DataBase.instance(collection_name)
        if not len(where):
            return False
        return collection.delete_one(where).deleted_count

    # удаление всех документов
    def delete_all(self, collection_name: str):
        collection = DataBase.instance(collection_name)
        return collection.remove({})

    # удаление данных
    def drop(self, collection_name: str):
        collection = DataBase.instance(collection_name)
        return collection.delete_many({}).deleted_count


if __name__ == '__main__':
    d = DataBase()
    print(d.select('mood'))