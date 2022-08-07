from sqlalchemy import DECIMAL, INTEGER, Boolean, Column, ForeignKey, Integer, String, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from internal import enums
from .database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    digits = Column(Integer, default=18)
    status = Column(String, default=enums.AssetStatus.active.value)


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    symbol = Column(String, primary_key=True, index=True)
    base_asset = Column(String, ForeignKey("assets.symbol"))
    base = relationship("Asset", foreign_keys=[base_asset])
    quote_asset = Column(String, ForeignKey("assets.symbol"))
    quote = relationship("Asset", foreign_keys=[quote_asset])
    base_precision = Column(Integer)
    quote_precision = Column(Integer)
    min_base_quantity = Column(DECIMAL(20, 18))
    min_quote_quantity = Column(DECIMAL(20, 18))
    status = Column(String)
