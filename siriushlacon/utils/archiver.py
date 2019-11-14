import datetime
import logging

import pytz
import requests

from siriushlacon.utils.alarm import Alarm, Severity
from siriushlacon.utils.consts import TIME_ZERO, SP_TZ, ARCHIVER_URL

logger = logging.getLogger()


def get_data_from_archiver(pv, from_, to=None, fetch_latest_metadata=True):
    """
    :param fetch_latest_metadata: if true, an extra call is made to the engine as part of the retrieval to get the
        latest values of the various fields (DESC, HIHI etc).
    :param pv: PV name
    :param from_: initial time UTC
    :param to: final time, defaults to the current time UTC
    :return: request HTTP response
    """
    if not from_:
        raise ValueError('cannot complete request, "_from" is not defined')

    if type(from_) == datetime.datetime:
        logger.debug('converting "from_" datetime.time to str')
        from_ = get_time_str_from_utc(from_)
    if type(to) == datetime.datetime:
        logger.debug('converting "to" datetime.time to str')
        to = get_time_str_from_utc(to)
    if not to:
        to = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
    params = {'pv': pv, 'to': to, 'from': from_, 'fetchLatestMetadata': 'true' if True else 'false'}

    req = requests.Request('GET', url=ARCHIVER_URL, params=params)
    prepared = req.prepare()
    logger.info('prepared request {} {}'.format(prepared.method, prepared.url))
    return requests.Session().send(prepared)


def get_time_str_from_utc(utc_time: datetime.datetime):
    """
    :param utc_time: datetime object
    :return: string formatted timestamp
    """
    if not utc_time.tzinfo:
        logger.warning('parameter "utc_time" does not have a timezone defined so UTC time will be assumed')
    else:
        if utc_time.utcoffset() != TIME_ZERO:
            logger.debug('parameter "utc_time" being converted to UTC time')
            utc_time = utc_time.astimezone(pytz.utc)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'


def print_entry(reading):
    # Timestamp
    print(datetime.datetime.fromtimestamp(reading['secs']).astimezone(SP_TZ))
    # Severity
    print('Severity ' + Severity.nameOf(reading['severity']))
    # Alarm Status
    print('Alarm ' + Alarm.nameOf(reading['status']))

    # Handle Value
    print(reading['val'])
    value = reading['val']

    # Considering a meaning per bit ...
    msgs = []
    map_ = {0: 'Zero', 1: 'One', 2: 'Two'}
    for k, v in map_.items():
        if value & 1 << k:
            msgs.append(v)
    print('{}'.format(msgs))

    print('\n')


if __name__ == '__main__':

    initial_time = datetime.datetime(2019, 1, 1, 0, 0, 0).astimezone(SP_TZ)
    response = get_data_from_archiver(pv='BO-01U:VA-SIP20-BG:SetErrorCode-Mon', from_=initial_time)
    if response.status_code == 200:
        for data in response.json()[0]['data']:
            print_entry(data)
    else:
        print('invalid status code')
