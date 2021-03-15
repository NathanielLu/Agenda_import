from db_table import db_table

if __name__ == '__main__':
    users = db_table("users", {"id": "integer PRIMARY KEY", "name": "text", "email": "text NOT NULL UNIQUE"})
    users.insert({"name": "Simon Ninon", "email": "simon.ninon@whova.com"})
    users.insert({"name": "Xinxin Jin", "email": "xinxin.jin@whova.com"})
    users.insert({"name": "Congming Chen", "email": "congming.chen@whova.com"})
    print(users.select())
    users.update({'name': 'John'}, {'id': 2})
    users.select(['name', 'email'], {'id': 2})
    print(users.close())
