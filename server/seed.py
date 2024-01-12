from app import app

from models import db, MakeupItem, Store, StoreHasItem

if __name__ == '__main__':
    with app.app_context():
        
        print("Clearing Out Tables...")

        MakeupItem.query.delete()
        Store.query.delete()
        StoreHasItem.query.delete()

        print("Seeding MakeupItem model...")

        new_makeup_items = [
            MakeupItem(
                name = "SatinAllure Lipstick",
                brand = "Pat McGrath Labs",
                type = "lipstick"
            ),
            MakeupItem(
                name = "Mini Soft Pinch Liquid Blush",
                brand = "Rare Beauty by Selena Gomez",
                type = "blush"
            ),
            MakeupItem(
                name = "They're Real! Lengthening Mascara",
                brand = "Benefit Cosmetics",
                type = "mascara"
            )
        ]

        db.session.add_all(new_makeup_items)

        print("Seeding Store model...")

        new_stores = [
            Store(
                name = "Sephora"
            ),
            Store(
                name = "Ulta"
            )
        ]

        db.session.add_all(new_stores)

        db.session.commit()

        print("Seeding StoreHasItem model...")

        new_joins = [
            StoreHasItem(
                item_id = new_makeup_items[0].id,
                store_id = new_stores[0].id,
                price = 30.00
            ),
            StoreHasItem(
                item_id = new_makeup_items[0].id,
                store_id = new_stores[1].id,
                price = 30.00
            ),
            StoreHasItem(
                item_id = new_makeup_items[1].id,
                store_id = new_stores[0].id,
                price = 14.00
            ),
            StoreHasItem(
                item_id = new_makeup_items[2].id,
                store_id = new_stores[1].id,
                price = 29.00
            )
        ]

        db.session.add_all(new_joins)

        db.session.commit()