import requests
import pytz
import datetime
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
    STATION_DATA_URL = 'https://na.chargepoint.com/dashboard/getChargeSpots?&lat=%.14f&lng=%.14f&ne_lat=%.14f' + \
                       '&ne_lng=%.14f&sw_lat=%.14f&sw_lng=%.14f'

    def __init__(self, username, password, latitude=DEFAULT_LATITUDE, longitude=DEFAULT_LONGITUDE):
        super(ChargePointScraper, self).__init__()
        self._cookies = None
        self._username = username
        self._password = password
        self._station_data_url = ChargePointScraper.STATION_DATA_URL % (
            latitude,
            longitude,
            latitude + ChargePointScraper.LATITUDE_DELTA,
            longitude + ChargePointScraper.LONGITUDE_DELTA,
            latitude - ChargePointScraper.LATITUDE_DELTA,
            longitude - ChargePointScraper.LONGITUDE_DELTA,
        )

    def get_station_data(self):
        if self._cookies is None:
            self._cookies = self._get_cookies()
        try:
            r = requests.get(self._station_data_url, cookies=self._cookies)
        except ConnectionError:
            raise ChargePointScraperException("Unable to connect to server.")
        try:
            data = r.json()
            if data[0]['user_info']['is_guest'] == 1:
                self._clear_cookies()
                raise ChargePointAuthenticationExpiredException()
            stations = data[0]['station_list']['summaries']
            return {
                'time': pytz.utc.localize(
                    datetime.datetime.strptime(data[0]['station_list']['time'], '%Y-%m-%d %H:%M:%S.%f')
                ).astimezone(
                    pytz.timezone("America/Los_Angeles")
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
            raise ChargePointScraperException("Unable to decode response.")
        except (IndexError, KeyError):
            raise ChargePointScraperException("Unexpected response json.")

    def _get_cookies(self):
        try:
            r = requests.post(ChargePointScraper.AUTH_URL, data={'user_name': self._username, 'user_password': self._password})
            if r.status_code != requests.codes.ok:
                raise ChargePointScraperException("Unexpected response status code.")
        except ConnectionError:
            raise ChargePointScraperException("Unable to connect to server.")
        try:
            data = r.json()
            if 'auth' in data and data['auth']:
                return r.cookies
            elif 'error' in data:
                raise ChargePointScraperException('Invalid login. Please try again.')
        except ValueError:
            raise ChargePointScraperException("Unable to decode response.")

    def _clear_cookies(self):
        self._cookies = None