from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class MakeupItem(db.Model, SerializerMixin):
    __tablename__ = "makeup_items"

    serialize_rules = ("-store_item.item",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    brand = db.Column(db.String)
    type = db.Column(db.String)

    store_item = db.relationship("StoreHasItem", back_populates="item")


class Store(db.Model, SerializerMixin):
    __tablename__ = "stores"

    serialize_rules = ("-item_stores.store",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    item_stores = db.relationship(
        "StoreHasItem",
        back_populates="store",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Failed name validation")
        return value


class StoreHasItem(db.Model, SerializerMixin):
    __tablename__ = "store_has_item"

    serialize_rules = ("-item.stores_item", "-store.item_stores")

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    item_id = db.Column(db.Integer, db.ForeignKey("makeup_items.id"))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))

    item = db.relationship("MakeupItem", back_populates="store_item")
    store = db.relationship("Store", back_populates="item_stores")

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Failed price validation")
        return value
