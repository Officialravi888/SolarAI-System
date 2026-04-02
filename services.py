import pandas as pd
from db import SessionLocal
from models import SolarData

def load_csv_to_db():
    db = SessionLocal()
    
    df = pd.read_csv("data/solar.csv")

    print(df.head())      # 🔥 debug
    print(df.columns)     # 🔥 debug

    for _, row in df.iterrows():
        data = SolarData(
            state=str(row["state"]),
            solar_generation=float(row["solar_output_kw"]),  # ✅ FIXED
            month="Feb"
        )
        db.add(data)

    db.commit()
    db.close()


def get_all_data():
    db = SessionLocal()
    data = db.query(SolarData).all()
    db.close()
    return data