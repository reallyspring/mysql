from classes.change import ChangeDB

db = ChangeDB()
db.connect()

# добавить пользователя
db.create("users", ["name", "email"], ["Иван", "ivan@mail.ru"])

# получить всех пользователей
users = db.read("users")
print(users)

# получить одного по id
user = db.read("users", condition="id = %s", params=[1])
print(user)

# поменять имя
db.update("users", {"name": "Петя"}, "id = %s", [1])

# удалить
db.delete("users", "id = %s", [1])

db.disconnect()