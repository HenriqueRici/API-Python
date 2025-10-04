from fastapi import APIRouter, HTTPException
from typing import List
from app.crud import servico as crud_servico
from app.models import Servico

router = APIRouter(
    prefix="/servicos",
    tags=["Servicos"]
)

@router.post("/", response_model=Servico, status_code=201)
def create_servico_endpoint(servico: Servico):
    try:
        return crud_servico.create_servico(servico)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=List[Servico])
def read_servicos_endpoint():
    return crud_servico.get_servicos()

@router.get("/{servico_id}", response_model=Servico)
def read_servico_endpoint(servico_id: int):
    db_servico = crud_servico.get_servico_by_id(servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Servico not found")
    return db_servico

@router.put("/{servico_id}", response_model=Servico)
def update_servico_endpoint(servico_id: int, servico: Servico):
    try:
        updated_servico = crud_servico.update_servico(servico_id, servico)
        if updated_servico is None:
            raise HTTPException(status_code=404, detail="Servico not found")
        return updated_servico
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{servico_id}", response_model=dict)
def delete_servico_endpoint(servico_id: int):
    result = crud_servico.delete_servico(servico_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Servico not found")
    return result