import logging

from starnavi.celery import app

logger = logging.getLogger('starnavi.console_logger')


@app.task
def add(x, y, *args, **kwargs):
    result = x + y
    logger.info('hello there %d' % result)
    return result
