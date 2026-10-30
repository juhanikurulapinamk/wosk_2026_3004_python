from users_sqlite_repository import UsersSQLiteRepository


def create_users_repository(con):
    return UsersSQLiteRepository(con)