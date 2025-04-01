from database import SessionLocal, URLMapping

db = SessionLocal()
urls = db.query(URLMapping).all()

if urls:
    print(f"Data found: {urls}")
else:
    print("No data found")

db.close