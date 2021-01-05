"""Feed Manager for VICEmergency Incidents feed."""
from typing import List, Tuple, Callable, Awaitable

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import VICEmergencyIncidentsFeed


class VICEmergencyIncidentsFeedManager(FeedManagerBase):
    """Feed Manager for VIC Emergency Incidents feed."""

    def __init__(self,
                 websession: ClientSession,
                 generate_callback: Callable[[str], Awaitable[None]],
                 update_callback: Callable[[str], Awaitable[None]],
                 remove_callback: Callable[[str], Awaitable[None]],
                 coordinates: Tuple[float, float],
                 filter_radius: float = None,
                 filter_inc_categories: List[str] = None,
                 filter_exc_categories: List[str] = None,
                 filter_statewide: bool = False,
                 status_callback: Callable[[StatusUpdate],
                                           Awaitable[None]] = None):
        """Initialize the VICEmergency Feed Manager."""
        feed = VICEmergencyIncidentsFeed(
            websession,
            coordinates,
            filter_radius=filter_radius,
            filter_inc_categories=filter_inc_categories,
            filter_exc_categories=filter_exc_categories,
            filter_statewide=filter_statewide)
        super().__init__(feed,
                         generate_callback,
                         update_callback,
                         remove_callback,
                         status_async_callback=status_callback)
