from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class MakeupItem(db.Model, SerializerMixin):
    __tablename__ = "makeup_items"

    serialize_rules = ('-store_item.item', )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    brand = db.Column(db.String)
    type = db.Column(db.String)

    store_item = db.relationship('StoreHasItem', back_populates = 'item')

class Store(db.Model, SerializerMixin):
    __tablename__ = "stores"

    serialize_rules = ('-item_store.store', )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    item_store = db.relationship('StoreHasItem', back_populates = 'store')

    '''
    @validates("name")
    def validate_name(self, key, value):
        if type(value) == str or isinstance(value, str):
            if len(value) > 0:
                return value
            else:
                raise ValueError
        else:
            raise ValueError
    '''

    @validates("name")
    def validate_name(self, key, value):
        if len(value) > 0:
            return value
        else:
            raise ValueError

class StoreHasItem(db.Model, SerializerMixin):
    __tablename__ = "store_has_item"

    serialize_rules = ('-item.store_item', '-store.item_store')

    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Float)

    item_id = db.Column(db.Integer, db.ForeignKey('makeup_items.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    item = db.relationship('MakeupItem', back_populates = 'store_item')
    store = db.relationship('Store', back_populates = 'item_store')

    '''
    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, float):
            raise ValueError
        elif value <= 0:
            raise ValueError
        else:
            return value
    '''

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError
        else:
            return value