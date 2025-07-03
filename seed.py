from market import app, db
from market.models import Item

def seed_items():
    sample_items = [
        Item(name="MacBook Pro", price=1999, barcode="123456789012", description="For coding and crying.", image="/static/images/laptop.jpg"),
        Item(name="Docker Mug", price=15, barcode="234567890123", description="Keeps your brain warm.", image="/static/images/mug.jpg"),
        Item(name="Flask Book", price=42, barcode="345678901234", description="Don't deploy things you barely understand. Haha, jk.", image="/static/images/book.jpg"),
    ]

    with app.app_context():
        # Optional: Clear existing entries
        num_deleted = Item.query.delete()
        print(f"Deleted {num_deleted} old items.")

        # Insert sample items
        db.session.add_all(sample_items)
        db.session.commit()
        print(f"Seeded {len(sample_items)} items.")
        

if __name__ == "__main__":
    seed_items()
