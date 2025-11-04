from fastapi import FastAPI
from app.api.endpoints import router as analyze_router

app = FastAPI(title="Review Analyzer API")
app.include_router(analyze_router, prefix="")

@app.get("/")
async def root():
    return {"message": "Welcome to Review Analyzer API"}
