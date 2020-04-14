# HA_AppDaemonZeverSolarSensor
Get power generation from ZeverSolar Inverter and present it to front end as a sensor for Hass.IO

## This AppDaemon application gets the generated solar power from a ZeverSolar Inverter and presents it to the front end of Hass.IO through a component.

![Image of Solar Panel](https://github.com/CheongKoo/HA_AppDaemonZeverSolarSensor/blob/master/images/ZeverSolar%20Panel.png?raw=true)

**Notes:**
1) Application is written for AppDaemon 3.
2) This will supersede my other project [HA_AppDaemonZeverSolar](https://github.com/CheongKoo/HA_AppDaemonZeverSolar) 
as that project uses MQTT. This is a simpler implementation and has no reliance on MQTT.
3) No changes need to be made to configuration.yaml as the component will appear to the Hass front end once it runs.
4) I am running my Hass.IO on a Raspberry Pi.
5) Reading is updated every 2 minutes (and this can be easily changed in the code).

**To implement this sensor:**
1) Install AppDaemon 3.
2) Configure AppDaemon and make sure that you can run the helloworld application.
3) Download this code and put it into the "/config/appdaemon/apps/" folder in your Hass.IO device.
4) In the code, you need to change the IP address to your ZeverSolar Inverter "zeverSolarURL".
5) Data is updated every 2 minutes. Change the value of "refreshInterval" to have a different value.
6) In your "/config/appdaemon/apps/apps.yaml" file, put in the following lines of code.
```
zeversolar_sensor:
  module: appd_ZeverSolarSensor
  class: ZeverSolarSensor
```

**How do you know if its working?**
1) In your AppDaemon log screen, you should be able to see the log as below:
![Image of AppDaemon log](https://github.com/CheongKoo/HA_AppDaemonZeverSolarSensor/blob/master/images/Appd_ZeverSolarSensor_log.py.png?raw=true)
2) In the Hass.IO, Developer Tools > States, you can see the below:
![Image of ZeverSolar entity](https://github.com/CheongKoo/HA_AppDaemonZeverSolarSensor/blob/master/images/DeveloperToolsStates.png?raw=true)

**Examples of images:**
![Image of Graph](https://github.com/CheongKoo/HA_AppDaemonZeverSolarSensor/blob/master/images/SolarGenerationGraph.png?raw=true)
![Image of Daily Generation](https://github.com/CheongKoo/HA_AppDaemonZeverSolarSensor/blob/master/images/Daily%20Generated%20Energy.png?raw=true)
