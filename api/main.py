from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from lib.db_engine import DbEngine
from schemas.receipt import Receipt

db = DbEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.initialize_db()
    yield
    db.delete_database()


app = FastAPI(lifespan=lifespan)


@app.post("/receipts/process")
async def process_receipts(receipt: Receipt):
    id = db.insert_one(receipt.__tablename__, receipt.model_dump())
    return {"id": id}


@app.get("/receipts/{id}/points")
async def get_points(id: str):
    receipt: Receipt = db.select_one("receipts", {"id": id})
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"points": receipt.get_points()}
