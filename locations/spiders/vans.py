from scrapy.http import JsonRequest
from scrapy.spiders import Spider

from locations.dict_parser import DictParser
from locations.hours import OpeningHours

DAYS_MAP = {
    "m": "Mo",
    "t": "Tu",
    "w": "We",
    "thu": "Th",
    "f": "Fr",
    "sa": "Sa",
    "su": "Su",
}


class VansSpider(Spider):
    name = "vans"
    item_attributes = {"brand": "Vans", "brand_wikidata": "Q1135366"}

    def start_requests(self):
        yield JsonRequest(
            url="https://www.vans.com/fapi/brandify/getCountriesList",
            data={
                "objectname": "Locator::Store",
                "where": {"and": {"or": {"off": {"eq": "TRUE"}, "out": {"eq": "TRUE"}}}},
                "limit": 0,
            },
        )

    def parse(self, response, **kwargs):
        for location in response.json()["response"]["collection"]:
            location["street_address"] = ", ".join(filter(None, [location.pop("address1"), location.pop("address2")]))

            item = DictParser.parse(location)

            item["ref"] = str(location["uid"])
            item["image"] = ";".join(
                filter(None, [location.get(f"imagepath")] + [location.get(f"imagepath{i}") for i in range(2, 6)])
            )

            item["extras"]["type"] = location["icon"]

            item["opening_hours"] = OpeningHours()
            for key, day in DAYS_MAP.items():
                if times := location.get(key):
                    if "closed" in times.lower():
                        continue
                    try:
                        start_time, end_time = times.split("-")
                        time_format = "%I:%M%p" if "AM" in times or "PM" in times else "%H:%M"
                        item["opening_hours"].add_range(day, start_time.strip(), end_time.strip(), time_format)
                    except:
                        pass

            yield item
