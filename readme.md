# Car Mileage Tracker

This is the start of an android application that will become my mental manager for the vehicle maintenance. I also wanted a project to learn object oriented programming as I am a novice. 

On my phone I will record the current mileage which is sent to my self hosted influxdb service via influx python API. This has a corresponding timestamp associated. You can also select a service from list and activate with checkbox (yes that needs to be moved below ha!) which is also recorded.

I have set this to the side for the moment to finish other projects but the back end is next. I will run a script on the server that compares last service item to current mileage and if service is required, it will use curl to send an alert VIA gotify to my phone. 

Demo here

https://odysee.com/@Haven_Labs:b/car_tracker_demo:9