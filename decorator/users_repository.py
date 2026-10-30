import sqlite3
from contextlib import closing


from factories.repositories import create_users_repository


def decorator_with_param(a):
    def decorator(route_handler):
        def wrapper(*args, **kwargs):
            return route_handler(a, *args, **kwargs)
        return wrapper
    return decorator


def get_users_repository(route_handler_func):

    def users_repository_wrapper(*args, **kwargs):
        with closing(sqlite3.connect("tuntiharjoitus1.db")) as con:
            repo = create_users_repository(con)

            return route_handler_func(repo, *args, **kwargs)
    return users_repository_wrapper


