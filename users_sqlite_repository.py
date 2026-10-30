import sqlite3

from custom_exceptions.not_found_exception import NotFoundException
from models import User


class UsersSQLiteRepository:
    # avataan tietokantayhteys luokan konstruktorissa

    # HUOM: tietokantayhteyden avaaminen kannattaa tehdä toisin
    # mutta käymme sen läpi vasta Dependency Injection-osiossa

    def __init__(self, con):
        self.connection = con

    def get_all(self):

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        users_list = []
        # Huomaa, että model classin metodi ei palauta hakutulosta suoraan json-formaatissa
        # Meidän pitää pystyä käyttämään samaa koodia riippumatta siitä,
        # haluaako käyttäjä vastauksen html, json- tai xml-formaatissa

        # Jos päättäisimme responsen formaatin modelissa,
        # joutuisimme tekemään uuden model-luokan metodin eri
        # dataformaateille.
        # Modelin tehtävä ei ole päättää tästä.
        # MODEL TOIMII TIETOMALLINA ja DATA ACCESS LAYERINÄ
        # ELI TULKKINA CONTROLLERIN JA TIETOKANNAN VÄLISSÄ

        for user in users:
            users_list.append(User(user[1], user[2], user[3], _id=user[0]))

        return users_list

    def _update(self, user):
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?  WHERE id = ?",
                        (user.firstname, user.lastname, user.username, user.id))
            self.connection.commit()
            cur.close()
        except Exception as e:
            self.connection.rollback()
            raise e

    def _insert(self, user):
        try:
            cur = self.connection.cursor()

            cur.execute("INSERT INTO users(first_name, last_name, username) VALUES(?, ?, ?)",
                        (user.firstname, user.lastname, user.username))
            self.connection.commit()
            user._id = cur.lastrowid

            cur.close()
        except Exception as e:
            self.connection.rollback()
            raise e

    def save(self, user):
        if user.id is None:
            self._insert(user)
        else:
            self._update(user)

    def get_by_id(self, _id):

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (_id,))
        existing_user = cur.fetchone()
        if existing_user is None:
            raise NotFoundException()
        return User(existing_user[1], existing_user[2], existing_user[3], _id=existing_user[0])

    def remove(self, _id):
        try:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (_id,))
            self.connection.commit()
            cur.close()
        except Exception as e:
            self.connection.rollback()
            raise e
