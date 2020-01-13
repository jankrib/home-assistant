"""Platform for light integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light
from homeassistant.const import CONF_IP_ADDRESS

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_IP_ADDRESS): cv.string, vol.Required("authkey"): cv.string}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    ip_address = config[CONF_IP_ADDRESS]
    authKey = config["authkey"]

    _LOGGER.info("Setup xComfort bridge: %s", ip_address)

    lights = [XComfortLight("Test")]

    # Add devices
    add_entities(lights)


class XComfortLight(Light):
    """Representation of an Awesome Light."""

    def __init__(self, name):
        """Initialize an AwesomeLight."""

        self._name = name
        self._state = None
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

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

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._state = True

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._state = False

    def update(self):
        pass
