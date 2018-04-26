from flask import Flask, request
import logging
from tg import Tg
from time import sleep

LOG_LEVEL = logging.DEBUG

logger = logging.getLogger("buildnotifier")
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


logger.info("Starting tg")
tg = Tg(logger=logger)

logger.info("Starting flask")
app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    data = request.json
    if data['type'] == 'build':
        logger.info('Data received: Starting build: ' + data['tag'])
        tg.send_build(data['tag'])
    if data['type'] == 'stage':
        logger.info('Data received: Running stage: ' + data['stage'])
        tg.send_stage(data['stage'])
    if data['type'] == 'complete':
        logger.info('Data received: Build complete: ' + data['url'])
        sleep(0.75)
        tg.send_complete(data['url'])
    return ''


@app.route('/health')
def healthcheck():
    return 'OK'
