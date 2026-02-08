from app import db  # or from your_app import db

db.drop_all()
db.create_all()
print("Database tables dropped and recreated successfully.")