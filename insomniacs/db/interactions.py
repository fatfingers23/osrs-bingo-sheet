"""
Contains behaviors for interacting with the database e.g.
  * Creating initial tables
  * Setting tile statuses
  * Other stuff
"""
import atexit
import mysql.connector
from insomniacs.configuration import DatabaseConfig, Tiles, Teams


class MysqlConnection(mysql.connector.connection.MySQLConnection):
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


def query_database(query):
    """
    Issues database query

    :param query: str representation of the query
    :param connection: The mySQL connection to query against
    :return: Results of the query
    """
    cursor = MysqlConnection().cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def init_table_from_config(config=Teams):
    """
    Creates a table based on a config


    | Team Name  | Tile1 | ... | TileN |
    | Chaos Rune | True  | ... | False |


    :param config: (dict) to generate the table schema
    :return: True if the table is successful generated, otherwise False
    """
    cursor = MysqlConnection().cursor(dictionary=True)

    clear_table = """
    DROP TABLE IF EXISTS bingo_data;
    """
    cursor.execute(clear_table)

    create_table = """
        CREATE TABLE bingo_data (
        TeamName VARCHAR(50)
        );
    """
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
