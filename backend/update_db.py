from app.database import engine
from sqlalchemy import text

def update_schema():
    print("Updating database schema...")
    with engine.connect() as conn:
        try:
            # Check if column exists (this is a simplified check, usually we'd query information_schema)
            # For this dev setup, we'll try to add it and catch the specific error if it exists,
            # or just execute the ALTER TABLE command.
            conn.execute(text("ALTER TABLE subscriptions ADD COLUMN usage_count INTEGER DEFAULT 0;"))
            conn.commit()
            print("Successfully added 'usage_count' column to 'subscriptions' table.")
        except Exception as e:
            print(f"Update failed (Column might already exist or other error): {e}")

if __name__ == "__main__":
    update_schema()
