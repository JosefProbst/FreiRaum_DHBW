#!/usr/bin/env python3

import connexion

from swagger_server import encoder
import swagger_server.controllers.database_controller as dbc
from flask_cors import CORS

def main():
    dbc.database = dbc.open_database()
    app = connexion.App(__name__, specification_dir='./swagger/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Freiraum Server RESTapi'})
    app.run(server="gevent", port=8080)


if __name__ == '__main__':
    main()
