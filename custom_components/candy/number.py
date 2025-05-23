import logging
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, DATA_KEY_COORDINATOR

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up Candy number entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_KEY_COORDINATOR]

    async_add_entities([
        CandyOvenTemperature(coordinator, config_entry),
        CandyOvenTime(coordinator, config_entry),
    ])

class CandyBaseNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": "Candy Oven",
            "manufacturer": "Candy",
        }

class CandyOvenTemperature(CandyBaseNumber):
    _attr_has_entity_name = True
    _attr_name = "Oven Temperature"
    _attr_unique_id = "candy_oven_temperature"
    _attr_entity_registry_enabled_default = True
    _attr_native_unit_of_measurement = "°C"
    _attr_native_min_value = 50
    _attr_native_max_value = 250
    _attr_native_step = 5
    _attr_mode = "slider"

    def __init__(self, coordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._attr_native_value = 180

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.debug("Set oven temperature to %s", value)
        self._attr_native_value = value
        self.async_write_ha_state()

class CandyOvenTime(CandyBaseNumber):
    _attr_has_entity_name = True
    _attr_name = "Oven Time"
    _attr_unique_id = "candy_oven_time"
    _attr_entity_registry_enabled_default = True
    _attr_native_unit_of_measurement = "min"
    _attr_native_min_value = 1
    _attr_native_max_value = 120
    _attr_native_step = 1
    _attr_mode = "box"

    def __init__(self, coordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._attr_native_value = 20

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.debug("Set oven time to %s", value)
        self._attr_native_value = value
        self.async_write_ha_state()
