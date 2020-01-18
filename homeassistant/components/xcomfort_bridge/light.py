"""Platform for light integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light
from homeassistant.const import CONF_IP_ADDRESS

from xcomfort import Bridge

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_IP_ADDRESS): cv.string, vol.Required("authkey"): cv.string}
)


async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    ip_address = config[CONF_IP_ADDRESS]
    auth_key = config["authkey"]

    _LOGGER.info("Setup xComfort bridge: %s", ip_address)

    bridge = await Bridge.connect(ip_address, auth_key)

    devices = await bridge.get_devices()

    lights = []

    for device_id in devices:
        lights.append(XComfortLight(bridge, devices[device_id]))

    # await bridge.close()

    await async_add_devices(lights)


class XComfortLight(Light):
    """Representation of an Awesome Light."""

    def __init__(self, bridge, device):
        """Initialize an AwesomeLight."""
        self._bridge = bridge
        self._device = device

        self._name = device.name
        self._state = device.switch
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def should_poll(self) -> bool:
        return True  # TODO Change to false and call schedule_update_ha_state() when state changes

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        await self._bridge.switch_device(self._device.device_id, True)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        await self._bridge.switch_device(self._device.device_id, False)
        self._state = False

    def update(self):
        pass
