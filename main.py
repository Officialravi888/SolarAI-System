from fastapi import FastAPI
from db import engine
from models import Base
from services import load_csv_to_db, get_all_data

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Solar API Running 🚀"}


@app.get("/load-data")
def load_data():
    load_csv_to_db()
    return {"message": "Data Loaded Successfully"}


@app.get("/data")
def fetch_data():
    data = get_all_data()
    return data