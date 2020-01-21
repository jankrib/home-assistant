"""Platform for light integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light
from homeassistant.const import CONF_IP_ADDRESS

from xcomfort import Bridge, Light as XLight
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Abode light devices."""
    bridge = hass.data[DOMAIN][entry.entry_id]

    if not isinstance(bridge, Bridge):
        _LOGGER.error(f"Invalid bridge. Got {bridge} for {entry.entry_id}")

    devices = await bridge.get_devices()

    lights = filter(lambda d: isinstance(d, XLight), devices.values())
    lights = map(lambda d: XComfortLight(bridge, d), lights)
    lights = list(lights)

    async_add_entities(lights)


class XComfortLight(Light):
    """Representation of an xComfort Light."""

    def __init__(self, bridge: Bridge, device: XLight):
        """Initialize an AwesomeLight."""
        super().__init__()

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
