import logging
import pkg_resources

logger = logging.getLogger()

try:
    f_name = pkg_resources.resource_filename(__name__, 'VERSION')
    with open(f_name) as _f:
        VERSION = _f.readline().strip('\n')
except FileNotFoundError:
    logger.exception('Unable fo locate {}'.format(f_name))
    VERSION = 'Undefined'
