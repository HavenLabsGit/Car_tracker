# Import my influx token
from apikeys import api_key

# Import kivy config for screen size
from pickle import FALSE
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', '0')

# fix the width of the window
Config.set('graphics', 'width', '325')

# fix the height of the window
Config.set('graphics', 'height', '500')
Config.set('graphics', 'fullscreen', '0')

# Import kivy requirements and KivyMD
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

# Import InfluxDB
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#==========================================================================#
#****************************** Variables *********************************#
#==========================================================================#

# Globals
global query
global miles

# Initalize values
miles = 0

# list of vehicles I want to track
vehicles = ("Honda", "Tundra", "T-100")

# boolean to know which car to record mileage
tundra = False
honda = False
t100 = False

#************************** InfluxDB variables *****************************#

token = api_key
org = "Permaculture Haven"
url = "https://influxdb.gardengifts.org"
bucket = "tester"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query = "To be replace"

# Initialize the influx queries
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)


#==========================================================================#
#****************************** Functions *********************************#
#==========================================================================#

def write_to_db(miles):
    if tundra == True:
        point = ((Point("Tundra").field("mileage", int(miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        print("Wrote Tundra")
    elif honda == True:
        point = ((Point("Honda").field("mileage", int(miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        print("Wrote Honda")
    elif t100 == True:
        point = ((Point("T-100").field("mileage", int(miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        print("Wrote T-100")
    else:
        print("Something went wrong!")



def build_query():

    results = [] # local varaible

    for x in vehicles:
        # Build flux query to grab mileage
        query = 'from(bucket:"tester")\
        |> range(start: -24h)\
        |> filter(fn:(r) => r._measurement == "'+ x +'")\
        |> filter(fn:(r) => r._field == "mileage")\
        |> last()'

        result = query_api.query(org=org, query=query)

        for table in result:
           for record in table.records:
             results.append((record.get_measurement(), record.get_value()))

    return results

#==========================================================================#
#******************************* Classes **********************************#
#==========================================================================#

class MainWindow(Screen):

    def selected_tundra(self):
        self.ids.tundra.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.t100.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.honda.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        global tundra, honda, t100
        tundra = True
        honda = False
        t100 = False
        print(tundra, honda, t100)

    def selected_t100(self):
        self.ids.t100.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.tundra.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.honda.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        global tundra, honda, t100
        tundra = False
        honda = False
        t100 = True
        print(tundra, honda, t100)

    def selected_honda(self):
        self.ids.honda.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.t100.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.tundra.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        global tundra, honda, t100
        tundra = False
        honda = True
        t100 = False
        print(tundra, honda, t100)

    def send_miles(self):
        miles = self.ids.mileage.text
        write_to_db(miles)


    def grab_mileage(self):
      mileage = build_query()
      print(mileage[0])
      print(mileage[1])
      print(mileage[2])

class Information(Screen):
    pass
class WindowManager(ScreenManager):
    pass



class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        kv = Builder.load_file('windows.kv')
        return kv


if __name__ == '__main__':

    MyApp().run()
