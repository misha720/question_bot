
import json
import os
import random



"""     
        Класс базы данных
"""



class DataBase:
    def __init__(self):

        # Проверка на присутствие
        if os.path.isfile('data.json'):
            # загружаем базу
            with open('data.json','r') as file_db:
                self.users = json.load(file_db)

    def save_base(self):
        with open('data.json', "w") as file_db:
            json.dump(self.users, file_db)

    def get_index_user(self, user_id):
        # Ищет пользавателя по id и возвращает индекс в базе
        for user_index, user_lot in enumerate(self.users):
            if user_id == user_lot['id']:
                return user_index
        return 0

    def create_user(self, user_id):
        # Создаёт нового пользователя
        new_user = {
            "id": int(user_id),
            "question":[]
        }

        self.users.append(new_user)

        self.save_base()