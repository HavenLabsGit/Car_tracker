from influx import Influx
from influxdb_client import Point, Dialect

miles = []

class GlobalVar():
    miles = 0
    car_num = 0
    results = ["Enter more recent data","Enter more recent data","Enter more recent data"]
    # list of vehicles I want to track
    vehicles =  "car"
    flag = False
    miles = [1]

# /* Name: write_to_db
#  * Parameter: int
#  * Return: nothing
#  * Description: Writes to selected bucket in influxdb. By knowing which car is selected (TRUE),
#  * will write to that vheicle and mileage entered in the field. We then set the car number
#  * to grab mileage for said car adn write to our list
#  */

class Write_to_db():

    def write_influx(self, car, service, miles):
        print(car)
        print(service)
        print(miles)
        point = ((Point(car).field(service, int(miles)))) # Create point to write to DB
        Influx.write_api.write(bucket=Influx.bucket, org=Influx.org, record=point) # Call API to write from influx class
            #GlobalVar.car_num = 1
        self.build_query(car)

# /* Name: build_query
#  * Parameter: none
#  * Return: list
#  * Description: Function queries influxdb bucket for mileage. Range goes back 1 month for now.
#  */

    def build_query(self, which_vehicle):

        # Build flux query to grab mileage
        query = 'from(bucket: "'+ Influx.bucket +'")\
        |> range(start: 2022-07-01T17:12:00.000Z, stop: 2023-08-18T17:12:27.731Z)\
        |> filter(fn:(r) => r._measurement == "'+ which_vehicle  +'")\
        |> filter(fn:(r) => r._field == "mileage")\
        |> distinct(column: "_value")'
        # execute query
        results = Influx.query_api.query(org=Influx.org, query=query)

        for table in results:
            print(table)
            for record in table.records:
                print(record.get_value())
                miles.append(record.get_value())
                return record.get_value()




    def work_query(self, which_vehicle):

        # Build flux query to grab mileage
        query = 'from(bucket: "'+ Influx.bucket +'")\
        |> range(start: 2022-07-01T17:12:00.000Z, stop: 2023-08-18T17:12:27.731Z)\
        |> filter(fn:(r) => r._measurement == "'+ which_vehicle  +'")\
        |> filter(fn:(r) => r._field == "mileage")\
        |> distinct(column: "_value")'
        # execute query
        data_frame = Influx.query_api.query_data_frame('from(bucket: "'+ Influx.bucket +'")\
            |> range(start: 2022-07-01T17:12:00.000Z, stop: 2023-08-18T17:12:27.731Z)\
            |> filter(fn:(r) => r._measurement == "'+ which_vehicle  +'")\
            |> drop(columns: ["_start", "_stop"])\
            |> distinct(column: "_value")')

        print(data_frame.to_string())

        # for table in results:
        #    for record in table.records:
        #     print(record.get_value())
        #     return record.get_value()
