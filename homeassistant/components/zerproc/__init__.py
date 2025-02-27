"""Zerproc lights integration."""

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DATA_ADDRESSES, DATA_DISCOVERY_SUBSCRIPTION, DOMAIN

PLATFORMS = [Platform.LIGHT]


async def async_setup(hass, config):
    """Set up the Zerproc platform."""
    hass.async_create_task(
        hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_IMPORT})
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Zerproc from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if DATA_ADDRESSES not in hass.data[DOMAIN]:
        hass.data[DOMAIN][DATA_ADDRESSES] = set()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Stop discovery
    unregister_discovery = hass.data[DOMAIN].pop(DATA_DISCOVERY_SUBSCRIPTION, None)
    if unregister_discovery:
        unregister_discovery()

    hass.data.pop(DOMAIN, None)

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
