# -HA_AppDaemonZeverSolarSensor
Get power generation from ZeverSolar Inverter and present it to front end as a sensor for Hass.IO

This AppDaemon application gets the generated solar power from a ZeverSolar Inverter and presents it to the front end of Hass.IO
through a component.

**Notes:**
1) Application is written for AppDaemon 3.
2) This will supersede my other project [HA_AppDaemonZeverSolar](https://github.com/CheongKoo/HA_AppDaemonZeverSolar) 
as that project uses MQTT. This is a simpler implementation and has no reliance on MQTT.
3) No changes need to be made to configuration.yaml as the component will appear to the Hass front end once it runs.
