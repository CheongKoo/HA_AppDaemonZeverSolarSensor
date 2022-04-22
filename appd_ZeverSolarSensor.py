#-------------------------------------------------------------------------------
# Name:        appd_ZeverSolarSensor.py
#
# Purpose:     To get the Zeversolar solar generation from the local website
#              and send it to the front end. It does it by sending it as a
#              sensor to the front end. This module parses the value returned
#              by the URL call and gives us the:
#              - Instantaneous generated power in kW
#              - Total generated energy for the day in kWH
#              You don't have to make any changes to your configuration.yaml file.
#              It automatically generates the sensor for the front end.
#
#              Note: Modified for AppDaemon 4
#
# Author:      Cheong Koo
#
# Created:     09/08/2021
#
# Note that at night, the server is down as there is no power hence need to check
# Below the reading from the URL separated by CR
# 1 1 EAB9618A0399 RSQMMVXNNPJMNWHY M11 17A31-727R+17829-719R 10:58 05/10/2019 0 1 BD500001018A0080 4978 14.52 OK Error
# 0 1      2             3           4           5              6       7      8 9        10         11    12  13   14
#
# In your "apps.yaml" file, put the following lines
# zeversolar_sensor:
#   module: appd_ZeverSolarSensor
#   class: ZeverSolarSensor
#-------------------------------------------------------------------------------

import hassapi as hass
import urllib.request
import datetime

# Check if server is up or down
# https://docs.python.org/3.1/howto/urllib2.html
from urllib.request import Request, urlopen
from urllib.error import  URLError
from datetime import datetime
from datetime import timedelta

#-------------------------------------------------------------------------------
# Global constants
# Get the below from Router
#-------------------------------------------------------------------------------
datetimeFormat = "%d/%m/%Y %H:%M" # Format for strftime()
generationFormat = "{:.2f}"
refreshInterval = 120 # Time interval to read the URL in seconds
genPowerIndex = 11 # Index into the returned string from the URL
dailyEnergyIndex = 12 # Index into returned string from the URL

#-------------------------------------------------------------------------------
# Inverter Class
#-------------------------------------------------------------------------------
class inverter:

    def __init__(self, name, ipaddr, generatedPower, totalEnergyDaily):
        self.name = name
        self.ipaddr = ipaddr
        self.httpaddr = "http://" + ipaddr + "/home.cgi"
        self.power = generatedPower
        self.energy = totalEnergyDaily

#-------------------------------------------------------------------------------
# Create inverter instances
# invXX = inverter('name', 'ipaddress'; 0, 0.0)
#-------------------------------------------------------------------------------
inv01 = inverter('garage_west_oben', '192.168.201.199', 0, 0.0)
inv02 = inverter('garage_west_unten', '192.168.201.76', 0, 0.0)

#-------------------------------------------------------------------------------
# Create inverter List variable
#-------------------------------------------------------------------------------
inv = [inv01, inv02]

#-------------------------------------------------------------------------------
# Class to be called by AppDaemon
# Remember to declare this class and the module in apps.yaml
#-------------------------------------------------------------------------------
class ZeverSolarSensorAll(hass.Hass):
    #---------------------------------------------------------------------
    #-- Initialise the module
    def initialize(self):
        self.log("------------------------------------------------", log="main_log")
        self.log("Initiatilize: ZeverSolar Sensor", log="main_log")
        #-- Intialise some local variables
        self.generatedPower = 0 # In W
        self.totalEnergyDaily = 0.00 # In KwH
        self.dateOfReading = datetime.now()
        #-- Run first time in 5 sec
        self.run_in(self.doGetGenAndSendAsSensor, 5)
        #-- Then run it every refreshInterval
        startTime = datetime.now() + timedelta(seconds=refreshInterval)
        self.run_every(self.doGetGenAndSendAsSensor,  startTime, refreshInterval)

    #---------------------------------------------------------------------
    #-- Get generation and send out as sensor
    def doGetGenAndSendAsSensor(self, arg):
        self.log("----- ZeverSolar sensor callback -----", log="main_log")

        # Call every inverter declared above
        for inverters in inv:
            # -- Get the generated power & energy
            #self.requestSolarGeneration(inverters.httpaddr)

            self.dateOfReading = datetime.now()  # Get date & time of reading
            req = Request(inverters.httpaddr)
            try:
                response = urlopen(req)
                htmlresponse = response.read()
                st = htmlresponse.decode()
                st = st.split()  # Convert the string into a list
                # -- Get the string for the Generated Power and Daily Energy
                genPower = st[genPowerIndex]
                dailyEnergy = st[dailyEnergyIndex]
                # -- Convert string into Int and Float
                inverters.power = int(genPower)  # Its in W eg. 4978
                # self.generatedPower = float(genPower)/1000 # Its in W eg. 4978. Convert into kW
                inverters.energy = float(dailyEnergy)  # It is already in kWh eg. 14.52
            except:
                self.log("Error in connecting to Zever solar server", log="main_log")
                inverters.power = 0
                inverters.energy = None


            lastUpdated = self.dateOfReading.strftime(datetimeFormat) # Last updated
            lastReset = self.dateOfReading.strftime("%Y-%m-%d 00:00:00+02:00")
            #-- Output the sensor values
            #-- Instantaneous Generated power
            stateInfo1 = generationFormat.format(inverters.power)
            self.set_state("sensor." + inverters.name +"_generated_power", state=stateInfo1, attributes=\
                            {"unit_of_measurement": "W", \
                            #-- "last_reset" : "1970-01-01T00:00:00+00:00", \
                            "last_reset" : lastReset, \
                            "state_class": "measurement", \
                            "device_class": "power", \
                            "icon": "mdi:white-balance-sunny", \
                            "friendly_name": "Generated Power",
                            "lastUpdated": lastUpdated
                             })
            #-- Daily energy generated
            #- Icons are located at http://materialdesignicons.com/
            stateInfo2 = generationFormat.format(inverters.energy)
            self.set_state("sensor." + inverters.name + "_daily_energy", state=stateInfo2, attributes=\
                            {"unit_of_measurement": "kWh", \
                            #-- "last_reset" : "1970-01-01T00:00:00+00:00", \
                            "last_reset" : lastReset, \
                            "state_class": "total_increasing", \
                            "device_class": "energy", \
                            "icon": "mdi:white-balance-sunny", \
                            "friendly_name": "Daily Generated Energy",
                            "lastUpdated": lastUpdated
                            })
            #-- Send out a log to the appdaemon console
            self.log("Updated: " + inverters.name + " at " + lastUpdated + " Gen: " + stateInfo1 + "W, Daily energy: " + stateInfo2 + "kWh", log="main_log")
