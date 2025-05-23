import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.select import SelectEntity

from .const import DOMAIN, DATA_KEY_COORDINATOR

_LOGGER = logging.getLogger(__name__)

PROGRAM_OPTIONS = [
    "Scongelamento",
    "Mantieni Caldo",
    "Statico",
    "Cottura Multilivello",
    "Inferiore Ventilato",
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Candy select platform from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_KEY_COORDINATOR]

    async_add_entities([
        CandyOvenProgramSelect(coordinator, config_entry.entry_id)
    ], True)


class CandyOvenProgramSelect(CoordinatorEntity, SelectEntity):
    """Select to choose Candy Oven program."""

    _attr_has_entity_name = True
    _attr_name = "Programma Forno"
    _attr_options = PROGRAM_OPTIONS
    _attr_unique_id = "candy_oven_programma"
    _attr_entity_registry_enabled_default = True

    def __init__(self, coordinator, config_id: str):
        super().__init__(coordinator)
        self._config_id = config_id
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_id)},
            "name": "Candy Oven",
            "manufacturer": "Candy",
        }

    @property
    def current_option(self) -> str:
        """Return the currently selected program.

        (qui potresti mappare da coordinator.data.program/selection al nome,
         per ora lasciamo il valore di default iniziale)
        """
        # di default 'Statico'
        return self._attr_options[2]

    async def async_select_option(self, option: str) -> None:
        """Handle the user selecting a new program."""
        _LOGGER.debug("Select new oven program: %s", option)
        # Qui salvi in un attributo interno, o in future config_entry.options
        # Per ora lo memorizziamo semplicemente:
        self._selected = option
        self.async_write_ha_state()
