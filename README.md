# ChargePoint Station Occupancy Scraper with Boxcar and OS X Notification Center support

by Nicholas Robinson

## Overview

This software allows for convenient monitoring of ChargePoint station occupancy via a text-based user interface. Additionally it supports OS X Notification center and Boxcar notifications, which are triggered whenever a new charging spot becomes available. This gives you a much needed advantage in an office charging environment where contention for charging spots is high!

## Requirements

* Python 2.7+
* Virtualenv
* OS X 10.8+ (for Notification Center)
* Boxcar account + compatible device (for Boxcar notifications)

## Installation

    $ git clone git://github.com/nicholasrobinson/ChargePoint-Scraper.git
    $ cd ChargePoint-Scraper/
    $ virtualenv v_env
	$ source v_env/bin/activate
	$ pip install -r requirements.txt
	$ vim main.py 
	(replace BOXCAR_ACCESS_TOKEN with your Boxcar access token)
	$ vim chargepoint_scraper.py
	(replace DEFAULT_LATITUDE and DEFAULT_LONGITUDE definitions with <YOUR_LATITUDE> and <YOUR_LONGITUDE>)

### Execution

	$ ./main.py
	(enter your ChargePoint username and password when prompted)
    
### Sample Output

                        SC-8#1  SC-8#2  SC-8#3  SC-8#4  SC-8#5  SC-8#6  SC-8#7  SC-8#8  SC-8#9  SC-8#10 SC-8#11 SC-10#1 SC-10#2 SC-10#3 SC-10#4 TA-7A#1 TA-7A#2 TA-7B#1 TA-7B#2
2015/06/06 17:32:43      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:33:43      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:34:44      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:35:45      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:36:45      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:37:46      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:38:46      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:39:47      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:40:48      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
2015/06/06 17:41:48      2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   1 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2   2 / 2 
    
### Sample Output Explanation

The above output shows 19 ChargePoint stations (indicated by the column headings) and their availability every minute (indicated by the row headings). The x/y entries in each cell indicate that x spots out of y total spots are currently unoccupied.

## References
    
* http://www.chargepoint.com/

## Notes

* In main.py the poll_chargepoint_stations(s) can be replaced with poll_chargepoint_stations(s, stations_of_interest=stations, stations_to_ignore=ignore) where stations_of_interest and stations_to_ignore kwargs allow you to specify stations you are interested in and/or would like to exclude.

Please let me know if you find this useful or come up with any novel implementations.

Enjoy!

Nicholas Robinson

me@nicholassavilerobinson.com