"""NSW Rural Fire Service Incidents feed entry."""
from markdownify import markdownify
import pytz
import calendar
from datetime import datetime
from time import strptime

import logging
import re
from typing import Optional, Tuple
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature
from markdownify import markdownify

from .consts import ATTR_CATEGORY1, ATTR_CATEGORY2, ATTR_DESCRIPTION, ATTR_ID, \
    ATTR_PUB_DATE,  ATTR_SOURCE_TITLE, ATTR_SOURCE_ORG, ATTR_ESTA_ID, \
    ATTR_RESOURCES, ATTRIBUTION, ATTR_SIZE, ATTR_SIZE_FMT, ATTR_LOCATION, \
    ATTR_STATEWIDE, ATTR_TEXT, ATTR_STATUS, ATTR_TYPE, ATTR_STATEWIDE, \
    ATTR_WEBBODY, CUSTOM_ATTRIBUTE

_LOGGER = logging.getLogger(__name__)

class VICEmergencyIncidentsFeedEntry(FeedEntry):
    """VIC Emergency Incidents feed entry."""

    def __init__(self,
                 home_coordinates: Tuple[float, float],
                 feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def attribution(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def title(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return ATTR_SOURCE_TITLE

    @property
    def category1(self) -> str:
        """Return the category of this entry."""
        return self._search_in_properties(ATTR_CATEGORY1)

    @property
    def category2(self) -> str:
        """Return the category of this entry."""
        return self._search_in_properties(ATTR_CATEGORY2)

    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        return self._search_in_properties(ATTR_ID)

    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        publication_date = self._search_in_properties(ATTR_PUB_DATE)
        if publication_date:
            # Parse the date. Sometimes that have Z as the timezone, which isn't like by %z.
            # This gets rids of any ms and the Z which then allows it to work.
            if publication_date[-1] == 'Z':
                date_struct = strptime(publication_date[:-5], "%Y-%m-%dT%H:%M:%S")
            else:
                date_struct = strptime(publication_date, "%Y-%m-%dT%H:%M:%S%z")

            publication_date = datetime.fromtimestamp(calendar.timegm(date_struct), tz=pytz.utc)
        return publication_date

    @property
    def description(self) -> str:
        """Return the description of this entry."""
        return self._search_in_properties(ATTR_TEXT)

    def _search_in_description(self, regexp):
        """Find a sub-string in the entry's description."""
        if self.description:
            match = re.search(regexp, self.description)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @property
    def location(self) -> str:
        """Return the location of this entry."""
        return self._search_in_properties(ATTR_LOCATION)

    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._search_in_properties(ATTR_STATUS)

    @property
    def type(self) -> str:
        """Return the type of this entry."""
        return self._search_in_properties(ATTR_TYPE)

    @property
    def size(self) -> str:
        """Return the size of this entry."""
        return self._search_in_properties(ATTR_SIZE)

    @property
    def size_fmt(self) -> str:
        """Return the size of this entry."""
        return self._search_in_properties(ATTR_SIZE_FMT)
    
    @property
    def statewide(self) -> str:
        """Return the size of this entry."""
        return self._search_in_properties(ATTR_STATEWIDE)

    @property
    def source_organisation(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_SOURCE_ORG)

    @property
    def source_organisation_title(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_SOURCE_TITLE)
    
    @property
    def resources(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_RESOURCES)

    @property
    def description(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_DESCRIPTION)

    @property
    def etsa_id(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_ESTA_ID)

    @property
    def advice_html(self) -> str:
        """Return the responsible agency of this entry."""
        return self._search_in_properties(ATTR_WEBBODY)

    @property
    def advice_markdown(self) -> str:
        """Return the responsible agency of this entry."""
        if self._search_in_properties(ATTR_WEBBODY) == None:
            return None
        return markdownify(self._search_in_properties(ATTR_WEBBODY))