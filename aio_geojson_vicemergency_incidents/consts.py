"""VIC Emergency Incidents constants."""

ATTR_CATEGORY1 = "category1"
ATTR_CATEGORY2 = "category2"
ATTR_DESCRIPTION = "description"
ATTR_ID = "id"
ATTR_PUB_DATE = "updated"
ATTR_SOURCE_TITLE = "sourceTitle"
ATTR_SOURCE_ORG = "sourceOrg"
ATTR_ESTA_ID = "estaid"
ATTR_RESOURCES = "resources"
ATTRIBUTION = "VICEmergency"
ATTR_SIZE = "size"
ATTR_SIZE_FMT = "sizefmt"
ATTR_LOCATION = "location"
ATTR_TEXT = "text"
ATTR_STATUS = "status"
ATTR_TYPE = "feedtype"
ATTR_STATEWIDE = "statewide"

CUSTOM_ATTRIBUTE = "custom_attribute"


URL = "http://emergency.vic.gov.au/public/osom-geojson.json"

VALID_CATEGORIES = [
    "Emergency Warning",
    "Watch and Act",
    "Advice",
    "Not Applicable"
]