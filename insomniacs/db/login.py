"""
Contains behavior related to supporting users.
"""
from flask_login import UserMixin
from insomniacs.db.queries import Query
from insomniacs.db.actions import query_database

import logging
import sys

logger = logging.getLogger("insomniacs.db.login")
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

USER_TABLE = "users"
USER_NAME_COL = "UserName"
PASSWORD_COL = "Password"


class User(UserMixin):
    def __init__(self, username, password=None):
        self.id = username
        self.username = username
        self.password = password

    def get_id(self):
        return self.username


def check_for_username(user: User):
    """
    Checks if the user's name appears in database

    :param user: User to check the name against
    :return: True if the name appears, otherwise False
    """
    if user is None:
        return False

    q = (Query().
         SELECT(USER_NAME_COL).FROM(USER_TABLE)
            .WHERE.EQUALS(USER_NAME_COL, "%s")
         )
    return query_database(q, (user.username,))[0][0]


def auth_user(user: User):
    """
    Queries the database to check the user exists with correct password

    :param user: The user account to check against the database
    :return: True if the username password combo appears in the database
    """
    q = f"""
        SELECT EXISTS(SELECT * FROM {USER_TABLE} WHERE {USER_NAME_COL}=%s AND {PASSWORD_COL}=%s);
    """
    return bool(query_database(q, (user.username, user.password))[0][0])
