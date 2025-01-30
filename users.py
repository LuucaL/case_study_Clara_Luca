import os
from tinydb import TinyDB, Query
from serializer import serializer

class User:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        self.id = id  # E-Mail-Adresse des Nutzers
        self.name = name  # Name des Nutzers

    def store_data(self) -> None:
        """Speichert den Benutzer in der Datenbank."""
        UserQuery = Query()
        existing_user = self.db_connector.search(UserQuery.id == self.id)
        if existing_user:
            self.db_connector.update({"name": self.name}, UserQuery.id == self.id)
        else:
            self.db_connector.insert({"id": self.id, "name": self.name})

    def delete(self) -> None:
        """Löscht den Benutzer aus der Datenbank."""
        UserQuery = Query()
        self.db_connector.remove(UserQuery.id == self.id)

    def __str__(self):
        return f"User: {self.name} ({self.id})"


    @staticmethod
    def find_all() -> list:
        """Findet alle Benutzer in der Datenbank."""
        users = []
        for user_data in User.db_connector.all():
            users.append(User(user_data['id'], user_data['name']))
        return users

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> 'User':
        """Findet Benutzer anhand eines Attributs."""
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery[by_attribute] == attribute_value)
        if result:
            data = result[0]
            return cls(data['id'], data['name'])
        return None
