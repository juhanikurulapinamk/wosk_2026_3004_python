from flask import jsonify, request

from custom_exceptions.not_found_exception import NotFoundException
from models import User
from users_sqlite_repository import UsersSQLiteRepository


def get_all_users_handler():
    try:
        repo = UsersSQLiteRepository()
        users = repo.get_all()
        # HUOM. tämä on esimerkki siitä, miten jsonin voi luoda
        # modelissa, mutta SE EI OLE SUOSITELTAVA TAPA,
        # koska modelin tehtävä ei ole huolehtia responsen content-typesta
        users_list = User.list_to_json(users)
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def add_new_user_handler():
    try:
        req_data = request.get_json()
        new_user = User(req_data['first_name'], req_data['last_name'], req_data['username'])
        repo = UsersSQLiteRepository()
        repo.save(new_user)
        return jsonify({'id': new_user.id, 'first_name': new_user.firstname, 'last_name': new_user.lastname,
                        'username': new_user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 409 CONFLICT


def update_user_handler(_id):
    try:
        repo = UsersSQLiteRepository()
        existing_user = repo.get_by_id(_id)
        req_data = request.get_json()
        new_first_name = req_data.get('first_name', existing_user.firstname)
        new_last_name = req_data.get('last_name', existing_user.lastname)
        new_username = req_data.get('username', existing_user.username)

        existing_user.firstname = new_first_name
        existing_user.lastname = new_last_name
        existing_user.username = new_username

        repo.save(existing_user)

        return jsonify(
            {'id': existing_user.id, 'first_name': existing_user.firstname, 'last_name': existing_user.lastname,
             'username': existing_user.username})




    except NotFoundException:
        return jsonify({'error': 'user not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500



def get_user_handler(_id):
    try:
        repo = UsersSQLiteRepository()
        existing_user = repo.get_by_id(_id)


        return jsonify(
            {'id': existing_user.id, 'first_name': existing_user.firstname, 'last_name': existing_user.lastname,
             'username': existing_user.username})




    except NotFoundException:
        return jsonify({'error': 'user not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_user_handler(_id):
    try:
        repo = UsersSQLiteRepository()
        existing_user = repo.get_by_id(_id)
        repo.remove(existing_user.id)

        return "", 204
        # affected_rows =  User.delete_by_id(_id)
        #if affected_rows == 0:
         #   return jsonify({'error': 'user not found'}), 404
    except NotFoundException:
        return jsonify({'error': 'user not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
