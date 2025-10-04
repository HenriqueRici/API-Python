from fastapi import FastAPI
from app.routers import colaborador, servico

app = FastAPI(
    title="Google Sheets CRUD API",
    description="An API to perform CRUD operations on Colaboradores and Servicos using Google Sheets as a database.",
    version="1.0.0"
)

# Include the routers from the separated files
app.include_router(colaborador.router, prefix="/api")
app.include_router(servico.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Google Sheets CRUD API"}