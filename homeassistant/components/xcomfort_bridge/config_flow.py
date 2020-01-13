"""Config flow for Eaton xComfort Bridge."""

import asyncio

from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import config_entry_flow
import voluptuous as vol
from collections import OrderedDict
from homeassistant.const import CONF_IP_ADDRESS

from .const import DOMAIN


class XComfortBridgeConfigFlow(data_entry_flow.FlowHandler):
    async def async_step_user(self, user_input):
        if user_input is not None:
            # TODO Validate user input

            return self.async_create_entry(
                title="Title of the entry",
                data={
                    CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS],
                    "authkey": user_input["authkey"],
                },
            )

        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_IP_ADDRESS)] = str
        data_schema[vol.Required("authkey")] = str

        return self.async_show_form(step_id="init", data_schema=vol.Schema(data_schema))

