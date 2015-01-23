#!/usr/bin/env python
import re
import requests
from requests.exceptions import ConnectionError
from time import sleep
from blessings import Terminal
from getpass import getpass
from sys import platform as _platform
if _platform == 'darwin':
    from pync import Notifier
from chargepoint_scraper import ChargePointScraper, ChargePointAuthenticationExpiredException, ChargePointScraperException


def naturally_sorted(_iterable):
    return sorted(_iterable, key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])


def send_boxcar_notification(title, message):
    payload = {
        'user_credentials': 'BOXCAR_ACCESS_TOKEN',
        'notification[title]': title,
        'notification[long_message]': message
    }
    try:
        requests.post('https://new.boxcar.io/api/notifications', data=payload)
    except ConnectionError:
        pass


def poll_chargepoint_stations(scraper, stations_of_interest=None, stations_to_ignore=None):
    if stations_to_ignore is None:
        stations_to_ignore = []
    if stations_of_interest is None:
        stations_of_interest = scraper.get_station_data()['stations'].keys()
    stations_of_interest = [x for x in stations_of_interest if x not in stations_to_ignore]
    old_free_spots = None
    old_open_stations = set()
    t = Terminal()
    try:
        i = 0
        while True:
            new_free_spots = 0
            new_open_stations = set()
            try:
                data = scraper.get_station_data()
            except ChargePointAuthenticationExpiredException:
                data = scraper.get_station_data()
            if i % 10 == 0:
                print '\t\t\t' + '\t'.join([station for station in stations_of_interest])
            line_parts = [data['time'].strftime('%Y/%m/%d %H:%M:%S')]
            for k in stations_of_interest:
                line_part = '%d / %d'.center(9) % (data['stations'][k]['available'], data['stations'][k]['total'])
                if data['stations'][k]['available'] == data['stations'][k]['total']:
                    line_part = t.black_on_green(line_part)
                elif data['stations'][k]['available'] == 0:
                    line_part = t.black_on_red(line_part)
                else:
                    line_part = t.black_on_yellow(line_part)
                line_parts.append(line_part)
                new_free_spots += data['stations'][k]['available']
                new_open_stations.add(k)
            print '\t'.join(line_parts)
            if old_free_spots is not None and new_free_spots != old_free_spots:
                title = '%s station(s) are open' % ', '.join(list(new_open_stations - old_open_stations))
                message = '%d Free Spots' % new_free_spots
                if _platform == 'darwin':
                    Notifier.notify(title=title, message=message)
                send_boxcar_notification(title=title, message=message)
            old_free_spots = new_free_spots
            old_open_stations = new_open_stations
            i += 1
            sleep(60)
    except KeyboardInterrupt:
        pass
    except KeyError:
        exit("Unexpected response json.")


if __name__ == '__main__':
    try:
        username = raw_input("username: ")
        password = getpass("password: ")
        s = ChargePointScraper(username, password) #, 37.3318, -122.0312)

        # Optional
        stations = filter(lambda x: 'SC-' in x or 'TA-7' in x, naturally_sorted(s.get_station_data()['stations'].keys()))
        ignore = ['MA-1#2']

        poll_chargepoint_stations(s, stations_of_interest=stations, stations_to_ignore=ignore)
    except ChargePointScraperException as e:
        exit(e.message)

