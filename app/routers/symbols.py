from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from orm import database, models
from internal import schemas, enums, middleware

router = APIRouter(
    prefix="/symbol",
    tags=["symbol"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.SymbolOut])
async def get_all(db: Session = Depends(database.get_db)):
    return db.query(models.Symbol).all()


@router.get("/{symbol}", response_model=schemas.SymbolOut)
async def get(symbol: str, db: Session = Depends(database.get_db)):
    db_symbol = db.query(models.Symbol).filter(
        models.Symbol.symbol == symbol
    ).first()
    if not db_symbol:
        raise HTTPException(status_code=404, detail="Not found")
    return db_symbol


@router.post("/", response_model=schemas.SymbolOut, dependencies=[Depends(middleware.verify_admin)])
async def create(symbol_in: schemas.SymbolIn, db: Session = Depends(database.get_db)):
    symbol = symbol_in.dict()
    symbol['symbol'] = f"{symbol_in.base_asset}{symbol_in.quote_asset}".upper(),
    symbol['status'] = enums.SymbolStatus.trading.value
    db_symbol = models.Symbol(**symbol)
    db.add(db_symbol)
    db.commit()
    db.refresh(db_symbol)
    return db_symbol
