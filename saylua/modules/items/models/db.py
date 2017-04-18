import re

from saylua import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True)
    url_name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))

    @classmethod
    def make_url_name(cls, name):
        name = re.sub(r'\s', '_', name)
        name = re.sub(r'\W', '-', name)
        return name.lower()

    @classmethod
    def by_url_name(cls, name):
        return cls.query(cls.url_name == name.lower()).get()

    def grant(cls, user_id, count):
        inventory_entry = InventoryItem.by_user_item(user_id, item.key)
        if not inventory_entry:
            inventory_entry = InventoryItem.construct(user_id, item)
        inventory_entry.count += count
        inventory_entry.put()


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    # These two keys define the inventory item entry.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    item = db.relationship("User")

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    item = db.relationship("Item")

    count = db.Column(db.Integer)
