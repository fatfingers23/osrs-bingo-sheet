"""
Parses and contains configuration data for use in other modules
"""
import configobj

config = configobj.ConfigObj("/etc/bingo_app.ini")


class DatabaseConfig:
    """
    Expected Database config values
    """
    USER = config["DATABASE"]["User"]
    PASSWORD = config["DATABASE"]["Password"]
    HOST = config["DATABASE"]["Host"]
    PORT = config["DATABASE"].as_int("Port")
    DATABASE = config["DATABASE"]["Database"]


Tiles = [(subsection, config["TILES"][subsection]["NumberDropsRequired"]) for subsection in config["TILES"].keys()]
Teams = config["TEAMS"].as_list("TeamNames")
