from flask import Flask, redirect, render_template, request


class Http:

    app = None

    def __init__(self, logger, callback):
        self.logger = logger

        logger.info("Starting flask")
        self.app = Flask(__name__)

        @self.app.route('/post', methods=['POST'])
        def post():
            data = request.json
            callback(data)
            return ''

        @self.app.route('/health')
        def healthcheck():
            return 'OK'

        self.app.run(host='0.0.0.0', port=5000, debug=True)
