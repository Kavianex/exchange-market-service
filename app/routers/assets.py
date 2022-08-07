from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from orm import database, models
from internal import schemas, middleware

router = APIRouter(
    prefix="/asset",
    tags=["asset"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetOut])
async def get_all(db: Session = Depends(database.get_db)):
    return db.query(models.Asset).all()


@router.get("/{symbol}", response_model=schemas.AssetOut)
async def get(symbol: str, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(
        models.Asset.symbol == symbol
    ).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Not found")
    return asset


@router.post("/", response_model=schemas.AssetOut, dependencies=[Depends(middleware.verify_admin)])
async def create(asset: schemas.AssetIn, db: Session = Depends(database.get_db)):
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    print("asset created!!")
    return db_asset
