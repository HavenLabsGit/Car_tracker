# Import my influx token
from __future__ import print_function
from pickle import TRUE
from apikeys import api_key

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
    honda_car_maintenance = {"Oil Change": 5000,
                             "Brake Fluid": 30000,
                             "Cooling Flush": 60000,
                             "Spark Plugs": 30000,
                             "Transmision Fluid": 60000,
                             "Spark Plugs": 110000}
    toyota_car_maintenance = {"Oil Change": 5000,
                             "Brake Fluid": 30000,
                             "Cooling Flush": 60000,
                             "Spark Plugs": 30000,
                             "Transmision Fluid": 60000,
                             "Spark Plugs": 110000,
                             "Timing Belt": 90000,
                             "Differential Oil": 30000,
                              "Transfer Case Oil": 30000}

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
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org,ssl=True, verify_ssl=False)
query = "To be replace"

# Initialize the influx queries
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)


#==========================================================================#
#****************************** Functions *********************************#
#==========================================================================#

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



honda_car= {"Oil Change": 133200, "Spark Plugs":110000}
last = 133000
current = 138900

# Set uo loop to go through maintenance items
for key in GlobalVar.honda_car_maintenance.keys():
    # create variable key to hold 1 dict key at a time
    if key in honda_car.keys():
        diff = current - last
        print(diff)
        if diff > (GlobalVar.honda_car_maintenance[key]):
            print("Service " + key)
        else:
            print("Nothing due")
