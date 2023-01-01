# Import my influx token
from ctypes import string_at
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
from kivy.app import App, StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.properties import StringProperty
# Import InfluxDB
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#==========================================================================#
#****************************** Variables *********************************#
#==========================================================================#

# Globals
class GlobalVar():
    miles = 0
    car_num = 0
    results = ["Enter more recent data","Enter more recent data","Enter more recent data"]
    # list of vehicles I want to track
    vehicles = ("Honda", "Tundra", "T-100")

class GlobalCar():
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

# /* Name: write_to_db
#  * Parameter: int
#  * Return: nothing
#  * Description: Writes to selected bucket in influxdb. By knowing which car is selected (TRUE),
#  * will write to that vheicle and mileage entered in the field. We then set the car number
#  * to grab mileage for said car adn write to our list
#  */

def write_to_db(miles):
    if GlobalCar.tundra == True:
        point = ((Point("Tundra").field("mileage", int(GlobalVar.miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        GlobalVar.car_num = 1
        build_query(GlobalVar.vehicles[GlobalVar.car_num])
    elif GlobalCar.honda == True:
        point = ((Point("Honda").field("mileage", int(GlobalVar.miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        GlobalVar.car_num = 0
        build_query(GlobalVar.vehicles[GlobalVar.car_num])
    elif GlobalCar.t100 == True:
        point = ((Point("T-100").field("mileage", int(GlobalVar.miles))))
        write_api.write(bucket=bucket, org=org, record=point)
        GlobalVar.car_num = 2
        build_query(GlobalVar.vehicles[GlobalVar.car_num])
# /* Name: build_query
#  * Parameter: none
#  * Return: list
#  * Description: Function queries influxdb bucket for mileage. Range goes back 1 month for now.
#  */

def build_query(which_vehicle):

        # Build flux query to grab mileage
        query = 'from(bucket:"tester")\
        |> range(start: -31d)\
        |> filter(fn:(r) => r._measurement == "'+ which_vehicle  +'")\
        |> filter(fn:(r) => r._field == "mileage")\
        |> last()'
        # execute query
        results = query_api.query(org=org, query=query)

        for table in results:
           for record in table.records:
             GlobalVar.results[GlobalVar.car_num]=(record.get_value())


def initalize_list(x):
        print(x)
        build_query(x)

#==========================================================================#
#******************************* Classes **********************************#
#==========================================================================#

class MainWindow(Screen):

    def selected_tundra(self):
        self.ids.tundra.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.t100.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.honda.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        GlobalCar.tundra = True
        GlobalCar.honda = False
        GlobalCar.t100 = False

    def selected_t100(self):
        self.ids.t100.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.tundra.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.honda.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        GlobalCar.tundra = False
        GlobalCar.honda = False
        GlobalCar.t100 = True

    def selected_honda(self):
        self.ids.honda.md_bg_color =(0.96, 0.43, 0.01, 0.5)
        self.ids.t100.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        self.ids.tundra.md_bg_color =(0.39, 0.85, 0.43, 0.5)
        GlobalCar.tundra = False
        GlobalCar.honda = True
        GlobalCar.t100 = False

    def send_miles(self):
        GlobalVar.miles = self.ids.mileage.text
        write_to_db(GlobalVar.miles)


    def grab_mileage(self):

        try:
            self.manager.get_screen('information').ids.honda.text = "Honda " + str(GlobalVar.results[0]) + " miles"
        except:
            self.manager.get_screen('information').ids.honda.text = "Enter more recent data"
        try:
            self.manager.get_screen('information').ids.tundra.text = "Tundra " + str(GlobalVar.results[1]) + " miles"
        except:
            self.manager.get_screen('information').ids.tundra.text = "Enter more recent data"
        try:
            self.manager.get_screen('information').ids.t100.text = "T-100 " + str(GlobalVar.results[2]) + " miles"
        except:
            self.manager.get_screen('information').ids.t100.text = "Enter more recent data"



class Information(Screen):
    pass
class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
   def build(self):
       self.theme_cls.theme_style="Dark"
       kv = Builder.load_file('windows.kv')
       return kv
   for x in GlobalVar.vehicles:                             # For how many vehilce
       initalize_list(x)
       GlobalVar.car_num+=1

if __name__ == '__main__':

    MyApp().run()
