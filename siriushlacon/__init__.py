import logging

logger = logging.getLogger()

try:
    with open('VERSION') as _f:
        VERSION = _f.readline().strip('\n')
except:
    logger.exception('Unable fo locate the VERSION file')
    VERSION = 'Undefined'
