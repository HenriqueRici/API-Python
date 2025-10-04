from fastapi import APIRouter, HTTPException
from typing import List
from app.crud import colaborador as crud_colaborador
from app.models import Colaborador

router = APIRouter(
    prefix="/colaboradores",
    tags=["Colaboradores"]
)

@router.post("/", response_model=Colaborador, status_code=201)
def create_colaborador_endpoint(colaborador: Colaborador):
    try:
        return crud_colaborador.create_colaborador(colaborador)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=List[Colaborador])
def read_colaboradores_endpoint():
    return crud_colaborador.get_colaboradores()

@router.get("/{colaborador_id}", response_model=Colaborador)
def read_colaborador_endpoint(colaborador_id: int):
    db_colaborador = crud_colaborador.get_colaborador_by_id(colaborador_id)
    if db_colaborador is None:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    return db_colaborador

@router.put("/{colaborador_id}", response_model=Colaborador)
def update_colaborador_endpoint(colaborador_id: int, colaborador: Colaborador):
    try:
        updated_colaborador = crud_colaborador.update_colaborador(colaborador_id, colaborador)
        if updated_colaborador is None:
            raise HTTPException(status_code=404, detail="Colaborador not found")
        return updated_colaborador
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{colaborador_id}", response_model=dict)
def delete_colaborador_endpoint(colaborador_id: int):
    result = crud_colaborador.delete_colaborador(colaborador_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    return result