import time
import datetime
import threading
import math
import json
import globals
from shapely.geometry import shape, Point
from pathlib import Path
try:
    import gps as gpsd_module
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False
    print("GPS NOT FOUND")
    exit()

#  ██████╗ ██████╗ ███████╗       ██╗      ██████╗  ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗                             
# ██╔════╝ ██╔══██╗██╔════╝       ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║                            
# ██║  ███╗██████╔╝███████╗       ██║     ██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║                            
# ██║   ██║██╔═══╝ ╚════██║       ██║     ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║                            
# ╚██████╔╝██║     ███████║       ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║                            
#  ╚═════╝ ╚═╝     ╚══════╝       ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

# The app was basically made for my hackberry and was not tested for other devices, 
# but probably this code works for every system that will run gpsd(GPS daemon).
# Basically all unix based systems Mac, Linux, Free BSD      
# Please notify me for any issues of bugs to fix or maybe even features to add ;)                                                                              

class gps_get():
    def __init__(self):
        self.lat = 0 
        self.lon = 0
        self.alt = 0
        self.laterr = 0
        self.lonerr = 0
        self.speed = 0
        self.speederr = 0
        self.fix = 0 #what type of fix the gps has
        self.time = "No time"  
        self.timeerr = 0
        self.heading = 0 
        self.climb = "N/A" #climb rate 
        self.session = None
        self.satelites = None
        self.usat = 0 #number of used satellites
        self.nsat = 0 #number of found satellites
        self.country_name = "Not found"
        self._is_set = threading.Event()
    def stop(self):
        self._is_set.set()
    def get_fix(self):
        if not GPS_AVAILABLE:
            return "Error: GPS NOT FOUND!"
        else:
            try:
                self.session = gpsd_module.gps(mode=gpsd_module.WATCH_ENABLE | gpsd_module.WATCH_NEWSTYLE)
                return True
            except Exception:
                return False
    def update_fix(self):
        while not self._is_set.is_set():
            if self.session is None:
                break
            try:
                for _ in range(20):
                    report = self.session.next()
                    if report['class'] == 'TPV': #looks for the TPV class data and updates the gps_get class
                        globals.fix   = getattr(report, 'mode',  1)
                        self.lat   = getattr(report, 'lat',   0)
                        self.lon   = getattr(report, 'lon',   0)
                        self.laterr = getattr(report, 'epy', "N/A")
                        self.lonerr = getattr(report, 'epx', "N/A")
                        self.alt   = getattr(report, 'alt',   "N/A")
                        self.speed = getattr(report, 'speed', 0)
                        self.speederr = getattr(report, 'eps', 0)
                        self.time = getattr(report, 'time', datetime.datetime.now())
                        self.timeerr = getattr(report, 'ept', "N/A")
                        self.heading = getattr(report, 'track', 0)
                        self.climb = getattr(report, 'climb', "N/A")
                    elif report['class'] == 'SKY': #looks for the SKY class data and updates the gps_get class
                        usat = getattr(report, 'uSat', None)
                        nsat = getattr(report, 'nSat', None)
                        satelites = getattr(report, 'satellites', [])
                        if nsat and usat != None:
                            self.nsat = nsat
                            self.usat = usat
                        if satelites != []:
                            self.satelites = satelites
                time.sleep(0.5)
            except Exception:
                print("Polling error")
    @property
    def has_fix(self):
        return self.fix >= 2 and self.lat is not None and self.lon is not None
    @property
    def get_head_str(self): #Cal    print(args.output)   # None if not providedculates the direction of travel from the heading that the gps module provides
        if self.heading is None:
            return "Not found"
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        directions_index = round(self.heading/45) % 8
        return f"{self.heading:.1f}", f"{directions[directions_index]}"
    @property
    def get_range_of_position(self):
        err = "N/A"
        if self.laterr and self.lonerr != "N/A":
            err = round(math.sqrt(self.laterr**2 + self.lonerr**2),1)
        return err
    @property
    def grid_square_position(self):
        if self.lon not in (0, "N/A") and self.lat not in (0, "N/A"):
            lon_adj = self.lon + 180
            lat_adj = self.lat + 90
            F1 = chr(ord('A') + int(lon_adj / 20))
            F2 = chr(ord('A') + int(lat_adj / 10))

            S1 = str(int((lon_adj % 20) / 2))
            S2 = str(int(lat_adj % 10))

            ss1 = chr(ord('a') + int((lon_adj % 2) * 12))
            ss2 = chr(ord('a') + int((lat_adj % 1) * 24))

            return F1 + F2 + S1 + S2 + ss1 + ss2
        else:
            return "Not found"
    
    def get_country(self): #Calculates which country the position give by the gps is based on the data in COUNTRY_BOUNDS
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent
        try:
            geojson_path = next(project_root.rglob("map.geojson"))
        except StopIteration:
            return "NO MAP FILE!"
        with open(geojson_path) as f:
            data = json.load(f)
        location = Point(self.lon, self.lat)
        features = data.get('features', [data])
        for feature in features:
            polygon = shape(feature['geometry'])
            if polygon.contains(location):
                country_name = feature.get('properties', {}).get('NAME', 'Unknown Country')
                self.country_name = country_name
                return country_name
        return "Ocean"


    def get_satelite_info(self):
        sat = []
        if self.satelites is not None:
            for satellite in self.satelites:
                sat.append((satellite.get('PRN', 0), satellite.get('used', False), satellite.get('ss', 0)))
            return sat
        return [("N/A", "N/A", "N/A")]
    def set_larp_values(self):
        self.lat = 21.3769420
        self.lon = 42.0967321
        self.alt = 276
        self.laterr = 10
        self.lonerr = 10
        self.speed = 0
        self.speederr = 0
        self.fix = 2 #what type of fix the gps has
        self.time = "21:37"  
        self.timeerr = 0.5
        self.heading = 0 
        self.climb = 0 #climb rate 
        self.session = None
        self.satelites = [
            {"PRN": 10, "el": 63, "az": 137, "ss": 17, "used": True},
            {"PRN": 7,  "el": 61, "az": 98,  "ss": 15, "used": True},
            {"PRN": 5,  "el": 59, "az": 290, "ss": 20, "used": True},
            {"PRN": 26, "el": 23, "az": 252, "ss": 0,  "used": True}
        ]
        self.usat = 4 #number of used satellites
        self.nsat = 4 #number of found satellites
        self.country_name = "STOP LARPING"

    
    

