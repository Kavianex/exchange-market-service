import pydantic
from orm import database, models
from . import enums


class Asset(pydantic.BaseModel):
    symbol: pydantic.types.constr(
        min_length=2, max_length=10, strip_whitespace=True)
    name: pydantic.types.constr(min_length=5, max_length=80)
    digits: pydantic.types.conint(gt=2, lt=19)

    class Config:
        orm_mode = True
        use_enum_values = True

    @staticmethod
    def get_asset(symbol: str) -> models.Asset | None:
        db = database.SessionLocal()
        asset = db.query(models.Asset).filter(
            models.Asset.symbol == symbol
        ).first()
        db.close()
        return asset


class AssetOut(Asset):
    status: enums.AssetStatus = enums.AssetStatus.active.value


class AssetIn(Asset):

    @pydantic.validator('symbol')
    def be_capital(cls, v):
        if not v == v.upper():
            raise ValueError("symbol must be upper case")
        return v

    @pydantic.validator('symbol')
    def unique_symbol(cls, v):
        db = database.SessionLocal()
        asset = db.query(models.Asset).filter(models.Asset.symbol == v).first()
        db.close()
        if asset:
            raise ValueError("symbol already exists!")
        return v


class Symbol(pydantic.BaseModel):
    base_precision: pydantic.types.conint(gt=0)
    quote_precision: pydantic.types.conint(gt=0)
    base_asset: str
    quote_asset: str
    min_base_quantity: pydantic.types.confloat(gt=0)
    min_quote_quantity: pydantic.types.confloat(gt=0)

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def is_new(cls, base_asset: str, quote_asset: str) -> bool:
        db = database.SessionLocal()
        symbol = db.query(models.Symbol).filter(
            models.Symbol.base_asset == base_asset,
            models.Symbol.quote_asset == quote_asset,
        ).first()
        db.close()
        return symbol is None


class SymbolOut(Symbol):
    symbol: str
    status: enums.SymbolStatus


class SymbolIn(Symbol):
    @pydantic.root_validator()
    def validate_precisions(cls, values):
        base_asset = values.get("base_asset", "")
        quote_asset = values.get("quote_asset", "")
        if not base_asset or not quote_asset:
            return values
        base_precision = int(values.get("base_precision", 1))
        base_asset = Asset.get_asset(base_asset)
        if base_asset.digits < base_precision:
            raise ValueError("base_precision is too big")
        quote_asset = Asset.get_asset(quote_asset)
        quote_precision = int(values.get("quote_precision", 1))
        if quote_asset.digits < quote_precision:
            raise ValueError("quote_precision is too big")
        if quote_asset.digits * base_asset.digits < quote_precision:
            raise ValueError("quote_precision is too big")
        if not cls.is_new(base_asset=base_asset.symbol, quote_asset=quote_asset.symbol):
            raise ValueError("symbol exsists")
        return values

    @pydantic.validator('base_asset', 'quote_asset', allow_reuse=True)
    def check_asset(cls, v):
        asset = Asset.get_asset(v)
        if not asset:
            raise ValueError("Asset does not exist!")
        elif not asset.status == enums.AssetStatus.active.value:
            raise ValueError("Asset is not active anymore!")
        return v
