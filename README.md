# python-aio-geojson-vicemergency-incidents

[![PyPi](https://img.shields.io/pypi/v/aio-geojson-vicemergency-incidents.svg)](https://pypi.python.org/pypi/aio-geojson-vicemergency-incidents)

This library provides convenient async access to the [VIC Emergency Website](https://www.emergency.vic.gov.au) incidents feed.

This code is based on [https://github.com/exxamalte/python-aio-geojson-nsw-rfs-incidents] by exxamalte.

## Installation

`pip install aio-geojson-vicemergency-incidents`

## Usage

See below for examples of how this library can be used. After instantiating a
particular class - feed or feed manager - and supply the required parameters,
you can call `update` to retrieve the feed data. The return value
will be a tuple of a status code and the actual data in the form of a list of
feed entries specific to the selected feed.

Status Codes

* _OK_: Update went fine and data was retrieved. The library may still return empty data, for example because no entries fulfilled the filter criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

### Parameters

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

### Supported Filters

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Include Categories | `filter_inc_categories` | Array of category names. Only include events with a category matching any of these is included. |
| Exclude Categories | `filter_exc_categories` | Array of category names. Exclude events with a category matching any of these is included. One example is previous burn areas from burning off, which have the category 'Burn Area' which last long after the event.|
| Statewide | `filter_statewide` | True or False. If set to true, will ignore statewide events (such as the COVID-19 pandemic advice) which doesn't change often and may not be necessary to include. |

### Example

```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_vicemergency_incidents import VicEmergencyIncidentsFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -37.813629, Longitude: 144.963058 (Elizabeth St in the CBD)
        # Filter radius: 50 km
        # Filter include categories: ''
        # Filter exclude categories: 'Burn Advice'
        # Filter statewide incidents: False 
        feed = VICEmergencyIncidentsFeed(websession, 
                                                (-37.813629, 144.963058), 
                                                filter_radius=50, 
                                                filter_inc_categories=[''],
                                                filter_exc_categories=['Burn Advice'],
                                                filter_statewide=False)
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties

Each feed entry is populated with the following properties:

| Name               | Description                                                                                         | Feed attribute |
|--------------------|-----------------------------------------------------------------------------------------------------|----------------|
| geometry           | All geometry details of this entry.                                                                 | `geometry`     |
| coordinates        | Best coordinates (latitude, longitude) of this entry.                                               | `geometry`     |
| external_id        | The unique public identifier for this incident.                                                     | `guid`         |
| title              | Title of this entry.                                                                                | `title`        |
| attribution        | Attribution of the feed.                                                                            | n/a            |
| distance_to_home   | Distance in km of this entry to the home coordinates.                                               | n/a            |

## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the consumer of the feed about new feed entries, updates and removed entries compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be reported as new. The feed manager will keep track of all feed entries' external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will produce three sets:
  * Feed entries that were not in the previous feed update but are in the current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update from the feed. This date may be useful if the consumer of this library wants to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest timestamp extracted from the feed data. This requires that the underlying feed data actually contains a suitable date. This date may be useful if the consumer of this library wants to process feed entries differently if they haven't actually been updated.
