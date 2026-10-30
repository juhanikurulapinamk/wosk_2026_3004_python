# app.py


from flask import Flask, jsonify, request

from controllers import users_controller

app = Flask(__name__)

""" Mikä tässä koodissa on vikana?

Jos tätä arvoidaan vain sillä perusteella, toimiiko kaikki, 
niin koodissa ei ole mitään vikaa, koska kaikki ominaisuudet
toimivat oikein

Arkkitehtuurin näkökulmasta koodi on aivan käyttökelvotonta.

Tehdään tämä seuraavaksi käyttäen MVC:tä.

"""

def some_function(a, b, c, d=0, e=0, f=0):
    pass

some_function("a", "b", "c", f=1, d=2, e=3)


# Hakee kaikki käyttäjät JSON-muodossa
app.add_url_rule('/api/users', 'get_all_users', users_controller.get_all_users_handler, methods=['GET'])
app.add_url_rule('/api/users', 'add_new_user', users_controller.add_new_user_handler, methods=['POST'])

# Hakee käyttäjän id:n perusteella
app.add_url_rule('/api/users/<_id>/<jokumuu>', 'get_user_by_id', users_controller.get_user_handler, methods=['GET'])

# Muokkaa id:n mukaan valitun käyttäjän tietoja
# request data lähetettävä JSON-muodossa
app.add_url_rule('/api/users/<_id>', 'update_existing_user', users_controller.update_user_handler,
                 methods=['PUT', 'PATCH'])

# Käyttäjän poisto id:n perusteella
app.add_url_rule('/api/users/<_id>', 'delete_existing_user', users_controller.delete_user_handler, methods=['DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
