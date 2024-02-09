from time import sleep
from flask import Flask, jsonify
from insomniacs.db.interactions import query_database, init_table_from_config


app = Flask(__name__, static_folder="/srv", static_url_path="/")
app.TABLE_CREATED = False

"""
@app.route('/')
def index():
    if not app.TABLE_CREATED:
        init_table_from_config()
        app.TABLE_CREATED = True
    return jsonify({'Test': query_database('SELECT TeamName FROM bingo_data')})

"""