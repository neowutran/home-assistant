"""
homeassistant.components.sensor.tellduslive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shows sensor values from Tellstick Net/Telstick Live.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.tellduslive/

"""
import logging
from datetime import datetime

from homeassistant.components import tellduslive
from homeassistant.const import (
    ATTR_BATTERY_LEVEL, DEVICE_DEFAULT_NAME, TEMP_CELCIUS)
from homeassistant.helpers.entity import Entity

ATTR_LAST_UPDATED = "time_last_updated"

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPE_TEMP = "temp"
SENSOR_TYPE_HUMIDITY = "humidity"
SENSOR_TYPE_RAINRATE = "rrate"
SENSOR_TYPE_RAINTOTAL = "rtot"
SENSOR_TYPE_WINDDIRECTION = "wdir"
SENSOR_TYPE_WINDAVERAGE = "wavg"
SENSOR_TYPE_WINDGUST = "wgust"
SENSOR_TYPE_WATT = "watt"

SENSOR_TYPES = {
    SENSOR_TYPE_TEMP: ['Temperature', TEMP_CELCIUS, "mdi:thermometer"],
    SENSOR_TYPE_HUMIDITY: ['Humidity', '%', "mdi:water"],
    SENSOR_TYPE_RAINRATE: ['Rain rate', 'mm', "mdi:water"],
    SENSOR_TYPE_RAINTOTAL: ['Rain total', 'mm', "mdi:water"],
    SENSOR_TYPE_WINDDIRECTION: ['Wind direction', '', ""],
    SENSOR_TYPE_WINDAVERAGE: ['Wind average', 'm/s', ""],
    SENSOR_TYPE_WINDGUST: ['Wind gust', 'm/s', ""],
    SENSOR_TYPE_WATT: ['Watt', 'W', ""],
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Sets up Tellstick sensors. """
    if discovery_info is None:
        return
    add_devices(TelldusLiveSensor(sensor) for sensor in discovery_info)


class TelldusLiveSensor(Entity):
    """ Represents a Telldus Live sensor. """

    def __init__(self, sensor_id):
        self._id = sensor_id
        self.update()
        _LOGGER.debug("created sensor %s", self)

    def update(self):
        """ update sensor values """
        tellduslive.NETWORK.update_sensors()
        self._sensor = tellduslive.NETWORK.get_sensor(self._id)

    @property
    def _sensor_name(self):
        return self._sensor["name"]

    @property
    def _sensor_value(self):
        return self._sensor["data"]["value"]

    @property
    def _sensor_type(self):
        return self._sensor["data"]["name"]

    @property
    def _battery_level(self):
        sensor_battery_level = self._sensor.get("battery")
        return round(sensor_battery_level * 100 / 255) \
            if sensor_battery_level else None

    @property
    def _last_updated(self):
        sensor_last_updated = self._sensor.get("lastUpdated")
        return str(datetime.fromtimestamp(sensor_last_updated)) \
            if sensor_last_updated else None

    @property
    def _value_as_temperature(self):
        return round(float(self._sensor_value), 1)

    @property
    def _value_as_humidity(self):
        return int(round(float(self._sensor_value)))

    @property
    def name(self):
        """ Returns the name of the device. """
        return "{} {}".format(self._sensor_name or DEVICE_DEFAULT_NAME,
                              self.quantity_name)

    @property
    def available(self):
        return not self._sensor.get("offline", False)

    @property
    def state(self):
        """ Returns the state of the device. """
        if self._sensor_type == SENSOR_TYPE_TEMP:
            return self._value_as_temperature
        elif self._sensor_type == SENSOR_TYPE_HUMIDITY:
            return self._value_as_humidity

    @property
    def device_state_attributes(self):
        attrs = {}
        if self._battery_level is not None:
            attrs[ATTR_BATTERY_LEVEL] = self._battery_level
        if self._last_updated is not None:
            attrs[ATTR_LAST_UPDATED] = self._last_updated
        return attrs

    @property
    def quantity_name(self):
        """ name of quantity """
        return SENSOR_TYPES[self._sensor_type][0]

    @property
    def unit_of_measurement(self):
        return SENSOR_TYPES[self._sensor_type][1]

    @property
    def icon(self):
        return SENSOR_TYPES[self._sensor_type][2]
