import random
import time
from datetime import datetime

from database import SessionLocal, engine, Base
from models import Crop, Market, Price


# Base realistic price ranges (₹ per quintal) for Karnataka-style demo
BASE_PRICE_RANGES = {
    "Maize": (1600, 2400),
    "Paddy": (1800, 2800),
    "Jowar": (2200, 3400),
    "Ragi": (2600, 4200),
    "Groundnut": (4000, 6500),
    "Cotton": (5200, 7800),
    "Tur Dal": (6500, 10500),
    "Onion": (800, 3000),
}


def generate_price_for_crop(crop_name: str):
    """
    Generates a realistic min/max/modal based on crop base range.
    """
    low, high = BASE_PRICE_RANGES.get(crop_name, (1000, 3000))

    # modal somewhere inside the range
    modal = random.uniform(low + (high - low) * 0.3, low + (high - low) * 0.7)

    # min and max around modal
    min_price = modal - random.uniform(50, 200)
    max_price = modal + random.uniform(50, 250)

    # safety clamp
    min_price = max(low, min_price)
    max_price = min(high, max_price)

    # keep logical ordering
    if min_price > modal:
        min_price = modal - 50
    if max_price < modal:
        max_price = modal + 50

    return round(min_price, 2), round(max_price, 2), round(modal, 2)


def apply_market_variation(price_value: float):
    """
    Adds small market-level variation (like demand, arrivals, local buyers).
    """
    variation = random.uniform(-0.04, 0.04)  # +/- 4%
    return price_value * (1 + variation)


def update_prices_once():
    """
    Updates all crop x market combinations in DB.
    """
    db = SessionLocal()

    crops = db.query(Crop).all()
    markets = db.query(Market).all()

    if not crops or not markets:
        print("❌ No crops/markets found. Run seed_data.py first.")
        db.close()
        return

    now = datetime.utcnow()

    for crop in crops:
        base_min, base_max, base_modal = generate_price_for_crop(crop.name)

        for market in markets:
            # Apply market variation
            min_p = apply_market_variation(base_min)
            max_p = apply_market_variation(base_max)
            modal_p = apply_market_variation(base_modal)

            # Fix ordering after variation
            min_p = min(min_p, modal_p)
            max_p = max(max_p, modal_p)

            # Store in DB
            p = Price(
                crop_id=crop.id,
                market_id=market.id,
                min_price=round(min_p, 2),
                max_price=round(max_p, 2),
                modal_price=round(modal_p, 2),
                updated_at=now
            )
            db.add(p)

    db.commit()
    db.close()

    print(f"✅ Prices updated for {len(crops)} crops x {len(markets)} markets @ {now}")


def run_engine(interval_seconds=30):
    """
    Runs continuous price update loop.
    """
    print("🚀 Dummy Price Engine Started")
    print(f"⏱ Updating every {interval_seconds} seconds...\n")

    while True:
        try:
            update_prices_once()
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n🛑 Dummy Price Engine Stopped")
            break
        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(interval_seconds)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    run_engine(interval_seconds=30)
