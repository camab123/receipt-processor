from fastapi import FastAPI

app = FastAPI()

@app.post("/receipts/process")
async def process_receipts():
    return {"message": "Processing receipts"}