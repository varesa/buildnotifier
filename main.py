import logging
from tg import Tg
from http import Http


LOG_LEVEL = logging.DEBUG

logger = logging.getLogger("buildnotifier")
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


logger.info("Starting")
Tg(logger=logger)


def callback(data):
    if data['type'] == 'build':
        logger.info('Data received: Starting build: ' + data['tag'])
        Tg.send_build(data['tag'])
    if data['type'] == 'stage':
        logger.info('Data received: Running stage: ' + data['stage'])
        Tg.send_stage(data['stage'])
    if data['type'] == 'complete':
        logger.info('Data received: Build complete: ' + data['url'])
        Tg.send_complete(data['url'])


Http(logger=logger, callback=callback)