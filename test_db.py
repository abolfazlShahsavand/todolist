from sqlalchemy import create_engine, text
from src.storage import DATABASE_URL

engine = create_engine(DATABASE_URL)
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Connected to database successfully!")
        row = conn.execute(text("SELECT current_database() AS db, current_user AS usr;")).mappings().one()
        print(f"🗃 DB: {row['db']} | 👤 User: {row['usr']}")
except Exception as e:
    print("❌ Database connection failed:", e)