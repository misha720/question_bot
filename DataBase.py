
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
        # Возвращает объект пользователя

        # Защита от букв в индексе
        try:
            key = int(user_id)

            if type(key) == int:
                # Ищет пользавателя по id и возвращает индекс в базе
                for user_index, user_lot in enumerate(self.users):
                    if key == user_lot['id']:
                        return user_index
            return None
        except:
            return None

    def create_user(self, user_id):
        # Создаёт нового пользователя
        new_user = {
            "id": int(user_id),
            "question":[]
        }

        self.users.append(new_user)

        self.save_base()