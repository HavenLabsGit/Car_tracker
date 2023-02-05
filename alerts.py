# Import my influx token
from __future__ import print_function
from apikeys import api_key

# Import InfluxDB
from influx import Influx
from influxdb_client import InfluxDBClient, Point, WritePrecision

import json

#==========================================================================#
#******************************* Classes **********************************#
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

    # /* Name: build_query
    #  * Parameter: none
    #  * Return: list
    #  * Description: Function queries influxdb bucket for mileage. Range goes back 1 month for now.
    #  */

    def build_query(self, vehicle):
        print( GlobalVar.vehicles[vehicle])
        # Build flux query to grab mileage
        query = 'from(bucket:"tester")\
        |> range(start: -61d)\
        |> filter(fn:(r) => r._measurement == "'+ GlobalVar.vehicles[vehicle] +'")\
        |> filter(fn:(r) => r._field == "mileage")\
        |> last()'
        # execute query
        results = Influx.query_api.query(org=Influx.org, query=query)

        for table in results:
           for record in table.records:
             GlobalVar.results[GlobalVar.car_num]=(record.get_value())

#==========================================================================#
#****************************** Functions *********************************#
#==========================================================================#


def grab_mileage():

    try:
        print("Honda " + str(GlobalVar.results[0]) + " miles")
    except:
        print("Enter more recent data")
    try:
        print("Tundra " + str(GlobalVar.results[1]) + " miles")
    except:
        print("Enter more recent data")
    try:
        print("T-100 " + str(GlobalVar.results[2]) + " miles")
    except:
        print("Enter more recent data")


def main():
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

    # Initalize class
    obj = GlobalCar()
    # Loop through function to grab all vehicles
    for x in range(0,3):
        obj.build_query(x)
        GlobalVar.car_num += 1
        print(x)
    grab_mileage()

if __name__ == '__main__':
    main() # This calls your main function

    print(json.dumps({"Honda":{"Oil Change": 133200, "Spark Plugs":110000}}))
