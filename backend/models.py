from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    markets = relationship("Market", back_populates="district")


class Market(Base):
    __tablename__ = "markets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))

    district = relationship("District", back_populates="markets")
    prices = relationship("Price", back_populates="market")


class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    prices = relationship("Price", back_populates="crop")


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)

    crop_id = Column(Integer, ForeignKey("crops.id"))
    market_id = Column(Integer, ForeignKey("markets.id"))

    min_price = Column(Float)
    max_price = Column(Float)
    modal_price = Column(Float)

    updated_at = Column(DateTime, default=datetime.utcnow)

    crop = relationship("Crop", back_populates="prices")
    market = relationship("Market", back_populates="prices")


class AuctionListing(Base):
    __tablename__ = "auction_listings"
    id = Column(Integer, primary_key=True, index=True)

    farmer_name = Column(String)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    market_id = Column(Integer, ForeignKey("markets.id"))

    quantity_quintal = Column(Float)
    quality_grade = Column(String)  # A/B/C
    expected_price = Column(Float)

    status = Column(String, default="ACTIVE")  # ACTIVE / CLOSED

    created_at = Column(DateTime, default=datetime.utcnow)
    ends_at = Column(DateTime)

    crop = relationship("Crop")
    market = relationship("Market")


class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True, index=True)

    auction_id = Column(Integer, ForeignKey("auction_listings.id"))
    buyer_name = Column(String)

    bid_price = Column(Float)
    bid_time = Column(DateTime, default=datetime.utcnow)
