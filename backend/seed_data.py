from database import SessionLocal, engine, Base
from models import District, Market, Crop


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Avoid duplicate seeding
    if db.query(District).count() > 0:
        print("✅ Seed data already exists. Skipping.")
        db.close()
        return

    districts = [
        "Gadag",
        "Belagavi",
        "Dharwad",
        "Bagalkot",
        "Haveri"
    ]

    crops = [
        "Maize",
        "Paddy",
        "Jowar",
        "Ragi",
        "Groundnut",
        "Cotton",
        "Tur Dal",
        "Onion"
    ]

    markets_map = {
        "Gadag": ["Gadag APMC", "Laxmeshwar Market"],
        "Belagavi": ["Belagavi APMC", "Gokak Market"],
        "Dharwad": ["Dharwad APMC", "Hubballi Market"],
        "Bagalkot": ["Bagalkot APMC", "Jamkhandi Market"],
        "Haveri": ["Haveri APMC", "Ranebennur Market"]
    }

    district_objs = {}
    for d in districts:
        obj = District(name=d)
        db.add(obj)
        district_objs[d] = obj

    db.commit()

    # Refresh to get IDs
    for d in district_objs.values():
        db.refresh(d)

    # Add markets
    for district_name, market_list in markets_map.items():
        district_obj = district_objs[district_name]
        for m in market_list:
            db.add(Market(name=m, district_id=district_obj.id))

    # Add crops
    for c in crops:
        db.add(Crop(name=c))

    db.commit()
    db.close()

    print("✅ Seed complete: districts, markets, crops added.")


if __name__ == "__main__":
    seed()
