"""
Contains behaviors for interacting with the database e.g.
  * Creating initial tables
  * Setting tile statuses
  * Other stuff
"""
import atexit
import mysql.connector
from enum import StrEnum
from insomniacs.configuration import DatabaseConfig, Tiles, Teams
from insomniacs.db.queries import Query, TEAM_TILE_QUERY

import sys
import logging
logger = logging.getLogger("insomniacs.db.interactions")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class TABLES(StrEnum):
    BINGO_DATA = "bingo_data"


class MysqlConnection(mysql.connector.connection.MySQLConnection):
    """
    Singleton pattern for MySQL connection. To prevent opening/closing a connection repeatedly.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = mysql.connector.connection.MySQLConnection(
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                database=DatabaseConfig.DATABASE,
            )
            # Put any initialization here.
        return cls._instance

    @staticmethod
    def on_shutdown():
        if MysqlConnection._instance is not None:
            MysqlConnection._instance.close()
            MysqlConnection._instance = None


# Provides automatic disconnection for the singleton pattern
atexit.register(MysqlConnection.on_shutdown)


def query_database(query: Query, params=None):
    """
    Issues database query

    :param query: str representation of the query
    :param params: Tuple of parameters to insert
    :return: Results of the query
    """
    cursor = MysqlConnection().cursor(buffered=True)
    cursor.execute(str(query), params=params)
    logger.debug("Running query_database with input:\n\t%s", cursor.statement)
    MysqlConnection().commit()
    results = cursor.fetchall()
    cursor.close()
    return results


def init_table_from_config(config=Teams):
    """
    Creates a table based on a config


    | Team Name  | Tile1 | ... | TileN |
    | Chaos Rune |   0   | ... |   0   |


    :param config: (dict) to generate the table schema
    :return: True if the table is successful generated, otherwise False
    """
    cursor = MysqlConnection().cursor(dictionary=True)
    cursor.execute(Query().DROP.TABLE.IF.EXISTS("bingo_data"))

    formatted_tiles = ",".join([f"{tile[0]} INT" for tile in Tiles])
    create_table = """
        CREATE TABLE bingo_data (
        TeamName VARCHAR(50),
        {formatted_tiles}
        );
    """
    create_table = str(
        Query().CREATE.TABLE("bingo_data").
            OPEN_P("TeamName").VARCHAR("(50)").COMMA(formatted_tiles)
            .CLOSE_P
    )
    cursor.execute(create_table)

    formatted_teams = ",".join([f"('{team}')" for team in Teams])
    populate_table = """
    INSERT INTO bingo_data
        (TeamName)
    VALUES
        {formatted_teams};
    """
    cursor.execute(populate_table.format(formatted_teams=formatted_teams))
    cursor.close()
    MysqlConnection().commit()


def get_tiles(team):
    """
    Grabs the current state of the given team's tiles

    :param team: Name of the team to get tiles for
    :return: dict of {<tile name>: <int representing completion>}
    """
    if team not in Teams:
        logger.error("%s is not in Teams (%s)", team, Teams)
        return None

    cursor = MysqlConnection().cursor(buffered=True)
    cursor.execute(TEAM_TILE_QUERY, (team,))
    logger.debug("Running get_tiles with input:\n\t%s", cursor.statement)
    results = dict(zip(cursor.column_names, cursor.fetchone()))
    cursor.close()
    return results
