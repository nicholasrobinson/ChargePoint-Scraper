import copy
import requests
import pytz
import datetime
import json
from requests.exceptions import ConnectionError


class ChargePointScraperException(Exception):
    pass


class ChargePointAuthenticationExpiredException(ChargePointScraperException):
    pass


class ChargePointScraper(object):
    # Office
    DEFAULT_LATITUDE = 37.32531489364759
    DEFAULT_LONGITUDE = -122.00501893998376

    LATITUDE_DELTA = 0.00255944575857
    LONGITUDE_DELTA = 0.00730097293854
    AUTH_URL = 'https://na.chargepoint.com/users/validate'
    STATION_DATA_URL = 'https://mc.chargepoint.com/map-prod/get?'
    STATION_DATA_QUERY_PARAMETERS = {
        'station_list': {
            'ne_lat': None,
            'ne_lon': None,
            'sw_lat': None,
            'sw_lon': None,
            'page_size': 100
        },
        'user_id': None
    }

    def __init__(self, username, password, latitude=DEFAULT_LATITUDE, longitude=DEFAULT_LONGITUDE):
        super(ChargePointScraper, self).__init__()
        station_data_query_parameters = copy.copy(ChargePointScraper.STATION_DATA_QUERY_PARAMETERS)
        station_data_query_parameters['station_list']['ne_lat'] = latitude + ChargePointScraper.LATITUDE_DELTA
        station_data_query_parameters['station_list']['ne_lon'] = longitude + ChargePointScraper.LONGITUDE_DELTA
        station_data_query_parameters['station_list']['sw_lat'] = latitude - ChargePointScraper.LATITUDE_DELTA
        station_data_query_parameters['station_list']['sw_lon'] = longitude - ChargePointScraper.LONGITUDE_DELTA
        station_data_query_parameters['user_id'] = ChargePointScraper._get_user_id(username=username, password=password)
        self._station_data_url = ChargePointScraper.STATION_DATA_URL + json.dumps(station_data_query_parameters).replace('"', '%22').replace(' ', '')

    @staticmethod
    def _get_user_id(username, password):
        try:
            r = requests.post(
                ChargePointScraper.AUTH_URL,
                data={
                    'user_name': username,
                    'user_password': password
                }
            )
            if r.status_code != requests.codes.ok:
                raise ChargePointScraperException('Unexpected response status code.')
        except ConnectionError:
            raise ChargePointScraperException('Unable to connect to server.')
        try:
            data = r.json()
            if 'auth' in data and data['auth'] and 'userid':
                return int(data['userid'])
            elif 'error' in data:
                raise ChargePointScraperException('Invalid login. Please try again.')
        except ValueError:
            raise ChargePointScraperException('Unable to decode response.')

    def get_station_data(self):
        try:
            r = requests.get(self._station_data_url)
        except ConnectionError:
            raise ChargePointScraperException('Unable to connect to server.')
        try:
            data = r.json()
            stations = data['station_list']['summaries']
            return {
                'time': pytz.utc.localize(
                    datetime.datetime.strptime(data['station_list']['time'], '%Y-%m-%d %H:%M:%S.%f')
                ).astimezone(
                    pytz.timezone('America/Los_Angeles')
                ),
                'stations':
                    {
                        station['station_name'][-1].replace(',', '').replace(' ', ''):
                            {
                                'available': station['port_count']['available'],
                                'total': station['port_count']['total']
                            }
                        for station in stations
                    }
            }
        except ValueError:
            raise ChargePointScraperException('Unable to decode response.')
        except (IndexError, KeyError):
            raise ChargePointScraperException('Unexpected response json.')
