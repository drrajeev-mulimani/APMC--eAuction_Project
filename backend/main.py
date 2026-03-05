from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal, engine, Base
from models import District, Market, Crop, Price

Base.metadata.create_all(bind=engine)

app = FastAPI(title="APMC eAuction MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "APMC eAuction MVP Backend Running"}


@app.get("/districts")
def get_districts(db: Session = Depends(get_db)):
    districts = db.query(District).all()
    return [{"id": d.id, "name": d.name} for d in districts]


@app.get("/markets")
def get_markets(db: Session = Depends(get_db)):
    markets = db.query(Market).all()
    return [{"id": m.id, "name": m.name, "district_id": m.district_id} for m in markets]


@app.get("/crops")
def get_crops(db: Session = Depends(get_db)):
    crops = db.query(Crop).all()
    return [{"id": c.id, "name": c.name} for c in crops]


@app.get("/prices/latest")
def latest_prices(db: Session = Depends(get_db)):
    prices = db.query(Price).order_by(Price.updated_at.desc()).limit(100).all()

    out = []
    for p in prices:
        out.append({
            "crop": p.crop.name,
            "market": p.market.name,
            "min": p.min_price,
            "max": p.max_price,
            "modal": p.modal_price,
            "updated_at": p.updated_at.isoformat()
        })
    return out
