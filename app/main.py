from fastapi import FastAPI
from app.routers import router

app = FastAPI(
    title="Google Sheets CRUD API",
    description="An API to perform CRUD operations on Colaboradores and Servicos using Google Sheets as a database.",
    version="1.0.0"
)

app.include_router(router, prefix="/api", tags=["api"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Google Sheets CRUD API"}