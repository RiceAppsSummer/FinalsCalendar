from app import db

def setup_all():
    setup_db()

def setup_db():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    setup_all()
