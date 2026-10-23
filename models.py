import sqlite3

from custom_exceptions.not_found_exception import NotFoundException


class User:
    def __init__(self, firstname, lastname, username, _id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self._id = _id

















    # JSON-tyyppimuunnoksia ei pitäisi tehdä modelissa,
    # koska model on malli datasta ja data access layer
    # controllerin tehtävä on hoitaa responsen parsiminen
    # TÄMÄ ON VAIN ESIMERKKI
    @staticmethod
    def list_to_json(users_list):
        json_list = []
        for user in users_list:
            json_list.append(user.to_json())
        return json_list

    # JSON-tyyppimuunnoksia ei pitäisi tehdä modelissa,
    # koska model on malli datasta ja data access layer
    # controllerin tehtävä on hoitaa responsen parsiminen
    # TÄMÄ ON VAIN ESIMERKKI
    def to_json(self):
        return {'id': self._id, 'firstname': self.firstname, 'lastname': self.lastname, 'username': self.username}

    @property
    def id(self):
        return self._id
