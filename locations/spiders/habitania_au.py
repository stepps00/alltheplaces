from locations.storefinders.metizsoft import MetizsoftSpider


class HabitaniaAUSpider(MetizsoftSpider):
    name = "habitania_au"
    item_attributes = {"brand": "Habitania", "brand_wikidata": "Q117923291"}
    shopify_url = "hab2015.myshopify.com"

    def parse_item(self, item, location):
        item.pop("website")
        yield item
