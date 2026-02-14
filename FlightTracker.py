import requests
import json
from pyfiglet import Figlet
from rich.console import Console
import time
import numpy as np

class Tracker():
    def __init__(self, lat, lon, radius_km, screen_orientation):
        # Base request URL
        url = 'https://api.adsb.lol'
        radius_nm = round(radius_km * 0.5399,3)
        self.lat = lat
        self.lon = lon
        self.screen_orientation = screen_orientation

        # API endpoints
        self.planes_url = f"{url}/v2/lat/{lat}/lon/{lon}/dist/{radius_nm}"
        self.single_plane_url = f"{url}/v2/closest/{lat}/{lon}/{radius_nm}"
        self.route_url = f"{url}/api/0/routeset"

        self.fig = Figlet(font="big")
        self.console = Console()


    def query_plane(self):
        closest_plane = json.loads(requests.get(self.single_plane_url).content)
        return closest_plane


    def query_route_info(self):
        # Route information query
        try:
            payload = {
                "planes": [
                    {
                    "callsign": self.closest_plane["ac"][0]["flight"].strip(), 
                    "lat": self.closest_plane["ac"][0]["lat"], 
                    "lng": self.closest_plane["ac"][0]["lon"]
                    }
                ]
            }
            self.route = requests.post(self.route_url, json=payload).json()

            airports_ticker = self.route[0]["_airport_codes_iata"].strip()
            airport_prov = self.route[0]["_airports"][0]["location"].strip()
            airport_dest = self.route[0]["_airports"][1]["location"].strip()

        except:
            airports_ticker = "Unknown"
            airport_prov = "Unknown"
            airport_dest = "Unknown"

        return airports_ticker, airport_prov, airport_dest


    def get_closest_plane_info(self):
        self.closest_plane = self.query_plane()
        # Try to get flight number first            
        
        if self.closest_plane["total"] == 0:
                return "No planes in range", " ", ".", "."
        else:  
            try:
                flight_nb = self.closest_plane["ac"][0]["flight"].strip()
            except:
                flight_nb = "Unknown"

            # Try to get route info, but don't overwrite flight_nb if route fails
            try:
                airports_ticker, airport_prov, airport_dest = self.query_route_info()
            except:
                airports_ticker = "Unknown"
                airport_prov = "Unknown"
                airport_dest = "Unknown"

            return flight_nb, airports_ticker, airport_prov, airport_dest



    def get_relative_pos_home(self):
        try:
            lat = self.closest_plane["ac"][0]["lat"]
            lon = self.closest_plane["ac"][0]["lon"]
            lat_dir = "N" if lat > self.lat else "S"
            lon_dir = "E" if lon > self.lon else "W"
            dlat = np.deg2rad(lat - self.lat)
            dlon = np.deg2rad(lon - self.lon)
            x = dlon * np.cos(np.deg2rad(self.lat))
            y = dlat

            bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360
            realative_bearing_screen = round((bearing - self.screen_orientation) % 360,1)
            relative_distance_km = round(np.sqrt(x**2 + y**2) * 6371,1)
        except:
            realative_bearing_screen = "."
            lat_dir = "."
            lon_dir = "."
            relative_distance_km = "."
            
        return realative_bearing_screen,lat_dir,lon_dir, relative_distance_km



    def render_console(self):
        while True:
            try:
                flight_nb, airports_ticker, airport_prov, airport_dest = self.get_closest_plane_info()
                relative_bearing_screen,lat_dir,lon_dir, relative_distance_km = self.get_relative_pos_home()

                arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]
                if relative_bearing_screen != "N/A" and isinstance(relative_bearing_screen, (int, float)):
                    if relative_bearing_screen < 22.5 or relative_bearing_screen >= 337.5:
                        arrow = arrows[0]  # N
                    elif relative_bearing_screen < 67.5:
                        arrow = arrows[1]  # NE
                    elif relative_bearing_screen < 112.5:
                        arrow = arrows[2]  # E
                    elif relative_bearing_screen < 157.5:
                        arrow = arrows[3]  # SE
                    elif relative_bearing_screen < 202.5:
                        arrow = arrows[4]  # S
                    elif relative_bearing_screen < 247.5:
                        arrow = arrows[5]  # SW
                    elif relative_bearing_screen < 292.5:
                        arrow = arrows[6]  # W
                    else:
                        arrow = arrows[7]  # NW
                else:
                    arrow = " "
                self.console.clear()

                # Big callsign
                banner = self.fig.renderText(airports_ticker or "NO FLIGHT")
                self.console.print(banner)

                # Info lines (smaller, colored, not ASCII art)
                self.console.print(f"[bold green]Flight Number:[/bold green] [white]{flight_nb}[/white]")
                self.console.print(f"[bold blue]From:[/bold blue] [white]{airport_prov}[/white]  [bold blue]→[/bold blue]  [white]{airport_dest}[/white]")
                self.console.print(f"[bold yellow]Relative position:[/bold yellow] [white]{relative_bearing_screen}° {arrow}[/white]")
                self.console.print(f"[bold cyan]Distance:[/bold cyan] [white]{relative_distance_km} km[/white]")

                time.sleep(5)

            except KeyboardInterrupt:
                self.console.clear()
                self.console.print("Stopped.")
                break

 



lat = 52.0                  # Current location latitude example
lon = 4.0                   # Current location longitude example
radius_km = 15              # Search radius in kilometers
screen_orientation = 26     # Screen orientation in degrees (back of the screen points to this bearing)


Plane = Tracker(lat, lon, radius_km, screen_orientation)
Plane.render_console()
