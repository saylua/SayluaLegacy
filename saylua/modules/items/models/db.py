from saylua import app, db
from saylua.utils import canonize, is_devserver, get_static_version_id
from flask import url_for
import os


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), unique=True)
    canon_name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))

    @classmethod
    def make_canon_name(cls, name):
        return canonize(name)

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()

    def url(self):
        return '/item/' + self.canon_name

    def image_url(self):
        return '/static/img/items/' + self.canon_name + '.png'
        if is_devserver():
            subpath = ("img" + os.sep + "items" + os.sep + self.canon_name + ".png")
            image_path = (os.path.join( # The joys of going up five levels
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(__file__)))), "static", subpath))
            if os.path.isfile(image_path):
                return url_for("static", filename=subpath) + "?v=" + str(get_static_version_id())
        return (app.config['IMAGE_BUCKET_ROOT'] + "/items/" + self.canon_name +
            ".png?v=" + str(get_static_version_id()))

    def grant(self, user_id, count):
        inventory_entry = InventoryItem.by_user_item(user_id, self.id)
        if not inventory_entry:
            inventory_entry = InventoryItem(user_id=user_id, item_id=self.id)
        inventory_entry.count += count
        inventory_entry.put()


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    # These two keys define the inventory item entry.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship("User")

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    item = db.relationship("Item")

    count = db.Column(db.Integer, default=0)
