from fastapi import FastAPI
from orm.database import engine, Base
from routers import assets, symbols
import uvicorn
import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(assets.router)
app.include_router(symbols.router)


@app.get("/")
async def root():
    return {"message": "OK!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT)
