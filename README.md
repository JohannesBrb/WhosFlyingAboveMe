# PlaneTracker

Track the closest airplane to your location in real time, right from your terminal! PlaneTracker uses open flight data APIs and displays flight info, route, in a colorful dashboard.


## Requirements
- Python 3.8+
- See requirements.txt for dependencies

## Installation
1. Clone this repository or download the files.
2. Install dependencies:
	```sh
	pip install -r requirements.txt
	```

## Usage
Edit the coordinates and screen orientation (direction in which the screen points back) in `FlightTracker.py`,  then run:
```sh
python3 FlightTracker.py
```

## Configuration
You can change the latitude, longitude, search radius, and screen orientation at the bottom of `FlightTracker.py`.

## Example Output
```
 _      _    _ _____               __  __  _____
| |    | |  | |  __ \        /\   |  \/  |/ ____|
| |    | |__| | |__) |_____ /  \  | \  / | (___
| |    |  __  |  _  /______/ /\ \ | |\/| |\___ \
| |____| |  | | | \ \     / ____ \| |  | |____) |
|______|_|  |_|_|  \_\   /_/    \_\_|  |_|_____/

Flight Number: BAW446
From: London  →  Amsterdam
Relative position: 261.6° ←
Distance: 14.1 km
```

## Data/API License
The flight data and API used (ADSB.lol) are licensed under the Open Data Commons Open Database License (ODbL) v1.0, the same license as OpenStreetMap.

For more information, see:
- [ODbL License](https://opendatacommons.org/licenses/odbl/1-0/)
- [ADSB.lol License Info](https://adsb.lol/license)

