from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = Session()  # Assuming this is a valid session
    try:
        yield db
    finally:
        db.close()


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return {"message": "Using the database session"}
