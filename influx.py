# My influxdb class


#==========================================================================#
#******************************* Imports **********************************#
#==========================================================================#

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from apikeys import api_key

#==========================================================================#
#******************************* CLasses **********************************#
#==========================================================================#

class Influx():
    token = api_key
    org = "Permaculture Haven"
    url = "https://influxdb.gardengifts.org"
    bucket = "test"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org,ssl=True, verify_ssl=False)
    query = "To be replace"
    Point="toyota"
    # Initialize the influx queries
    query_api = client.query_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)
