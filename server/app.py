from config import app
from flask import make_response, request
from flask_restful import Api, Resource

from models import db, MakeupItem, Store, StoreHasItem

@app.route('/makeup_items', methods = ['GET'])
def makeup_items():
    makeup_items_dict = [item.to_dict(rules = ('-store_item', )) for item in MakeupItem.query.all()]

    response = make_response(
        makeup_items_dict,
        200
    )

    return response

@app.route('/stores', methods = ['GET', 'POST'])
def stores():
    if request.method == 'GET':
        stores = Store.query.all()

        stores_dict = [store.to_dict() for store in stores]

        response = make_response(
            stores_dict,
            200
        )
    elif request.method == 'POST':
        try:
            form_data = request.get_json()

            new_store = Store(
                name = form_data['name']
            )

            db.session.add(new_store)
            db.session.commit()

            response = make_response(
                new_store.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"Error" : "Validations issue raised when creating Store object!"},
                400
            )

    return response

@app.route('/stores/<int:id>', methods = ['GET', 'DELETE'])
def store_by_id(id):
    selected_store = Store.query.filter(Store.id == id).first()

    if selected_store:
        if request.method == 'GET':
            response = make_response(
                selected_store.to_dict(rules = ('-item_store', )),
                200
            )
        elif request.method == 'DELETE':
            assoc_joins = StoreHasItem.query.filter(StoreHasItem.store_id == id).all()

            for assoc_join in assoc_joins:
                db.session.delete(assoc_join)

            db.session.delete(selected_store)

            db.session.commit()

            response = make_response(
                {},
                204
            )
    else:
        response = make_response(
            {"Error" : "Store object not found!"},
            404
        )

    return response

@app.route('/store_has_item/<int:id>', methods = ['PATCH'])
def store_has_item_by_id(id):
    selected_shi = StoreHasItem.query.filter(StoreHasItem.id == id).first()

    if selected_shi:
        try:
            form_data = request.get_json()

            for attr in form_data:
                setattr(selected_shi, attr, form_data[attr])

            db.session.commit()

            response = make_response(
                selected_shi.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"Error" : "Validations issue raised when creating StoreHasItem object!"},
                400
            )
    else:
        response = make_response(
            {"Error" : "StoreHasItem object not found!"},
            404
        )

    return response

if __name__ == "__main__":
    app.run(port = 5555, debug = True)