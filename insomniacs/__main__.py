"""
Currently just runs the app

TODO: Add flag parsing support for CLI configurability
"""
from insomniacs.app import app

app.run(host='0.0.0.0')
