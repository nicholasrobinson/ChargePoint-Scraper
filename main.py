#!/usr/bin/env python
import re
from time import sleep
from blessings import Terminal
from pync import Notifier
from getpass import getpass
from chargepoint_scraper import ChargePointScraper, ChargePointAuthenticationExpiredException, ChargePointScraperException


def naturally_sorted(_iterable):
    return sorted(_iterable, key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])


def poll_chargepoint_stations(scraper, stations_of_interest=None, stations_to_ignore=None):
    if stations_to_ignore is None:
        stations_to_ignore = []
    if stations_of_interest is None:
        stations_of_interest = scraper.get_station_data()['stations'].keys()
    stations_of_interest = [x for x in stations_of_interest if x not in stations_to_ignore]
    old_free_spots = None
    t = Terminal()
    try:
        i = 0
        while True:
            new_free_spots = 0
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
            print '\t'.join(line_parts)
            if old_free_spots is not None and new_free_spots != old_free_spots:
                Notifier.notify('%d Free Spots' % new_free_spots, title="ChargePoint Monitor")
            old_free_spots = new_free_spots
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

