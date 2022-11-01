from database import Session


def get_context_db():
    db = Session()
    try:
        yield db
    finally:
        db.close
