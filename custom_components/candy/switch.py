import asyncio
import aiohttp
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_registry import async_get as async_get_registry

from .const import DOMAIN, DATA_KEY_COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the Candy switch platform from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_KEY_COORDINATOR]
    async_add_entities([CandyOvenPowerSwitch(coordinator, config_entry)], True)


class CandyOvenPowerSwitch(CoordinatorEntity, SwitchEntity):
    """Switch to control Candy Oven power."""

    _attr_has_entity_name = True
    _attr_name = "Power"
    _attr_unique_id = "candy_oven_power"
    _attr_entity_registry_enabled_default = True

    def __init__(self, coordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": "Candy Oven",
            "manufacturer": "Candy",
        }

    @property
    def is_on(self) -> bool:
        status = self.coordinator.data
        return str(status.machine_state).lower() == "heating"

    async def async_turn_on(self, **kwargs) -> None:
        ip = getattr(self.coordinator, "device_ip", None)
        if not ip:
            _LOGGER.error("No IP address available, cannot turn on oven")
            return

        # Recupera l'entity_id dai unique_id delle number entitites
        registry = async_get_registry(self.hass)
        temp_eid = registry.async_get_entity_id("number", DOMAIN, "candy_oven_temperature")
        time_eid = registry.async_get_entity_id("number", DOMAIN, "candy_oven_time")

        temp_state = self.hass.states.get(temp_eid) if temp_eid else None
        time_state = self.hass.states.get(time_eid) if time_eid else None

        if not temp_state or not time_state:
            _LOGGER.error("Missing number entities: %s / %s", temp_eid, time_eid)
            return

        try:
            temp = float(temp_state.state)
            time_val = int(float(time_state.state))
        except ValueError as e:
            _LOGGER.error("Error parsing number entities: %s", e)
            return

        temp_set = int(temp * 10)
        params = (
            f"Write=1"
            f"&Selettore=4"
            f"&Program=4"
            f"&TempSet={temp_set}"
            f"&TimeProgr={time_val}"
            f"&StartStop=1"
        )
        url = f"http://{ip}/http-write.json?{params}"
        _LOGGER.debug("Sending ON command: %s", url)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    _LOGGER.debug("ON response: %s", await resp.text())
        except Exception as e:
            _LOGGER.error("Error sending ON command: %s", e)

        await asyncio.sleep(1.5)
        await self.coordinator.async_request_refresh()
        await asyncio.sleep(0.5)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        ip = getattr(self.coordinator, "device_ip", None)
        if not ip:
            _LOGGER.error("No IP address available, cannot turn off oven")
            return

        url = f"http://{ip}/http-write.json?Write=1&StartStop=0"
        _LOGGER.debug("Sending OFF command: %s", url)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    _LOGGER.debug("OFF response: %s", await resp.text())
        except Exception as e:
            _LOGGER.error("Error sending OFF command: %s", e)

        await asyncio.sleep(1.5)
        await self.coordinator.async_request_refresh()
        await asyncio.sleep(0.5)
        self.async_write_ha_state()



########################################################### da completare dopo comando programmi funzionante 

# # dentro CandyOvenPowerSwitch.async_turn_on
# program_state = self.hass.states.get("select.candy_oven_programma").state
# # mappa program_state → Selettore e Program numerici
# if program_state == "Scongelamento":
#     sel, pr = 2, 3
# elif program_state == "Mantieni Caldo":
#     sel, pr = 3, 7
# # … ecc …

# params = f"Write=1&Selettore={sel}&Program={pr}&TempSet={temp_set}&TimeProgr={time_val}&StartStop=1"
# url = f"http://{ip}/http-write.json?{params}"


