class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __str__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"

# Item Behaviors

class ItemBehavior:
    def __init__(self, item: Item):
        self.item = item

    def tick(self):
        self.decrease_sell_in()
        self.update_quality()

    def decrease_sell_in(self):
        self.item.sell_in -= 1

    def update_quality(self):
        if self.item.sell_in < 0:
            self.change_quality(-2)  # after expiry, degrade twice as fast
        else:
            self.change_quality(-1)

    def change_quality(self, delta):
        self.item.quality = max(0, min(50, self.item.quality + delta))


class SulfurasBehavior(ItemBehavior):
    def tick(self):
        pass  # never changes


class AgedBrieBehavior(ItemBehavior):
    def update_quality(self):
        if self.item.sell_in < 0:
            self.change_quality(+2)
        else:
            self.change_quality(+1)


class BackstagePassBehavior(ItemBehavior):
    def update_quality(self):
        if self.item.sell_in < 0:
            self.item.quality = 0
        elif self.item.sell_in < 5:
            self.change_quality(+3)
        elif self.item.sell_in < 10:
            self.change_quality(+2)
        else:
            self.change_quality(+1)

# Behavior Factory

class ItemBehaviorFactory:
    @staticmethod
    def get_behavior(item: Item) -> ItemBehavior:
        if item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasBehavior(item)
        elif item.name == "Aged Brie":
            return AgedBrieBehavior(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassBehavior(item)
        else:
            return ItemBehavior(item)

class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            behavior = ItemBehaviorFactory.get_behavior(item)
            behavior.tick()
