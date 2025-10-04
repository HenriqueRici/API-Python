from fastapi import APIRouter, HTTPException
from typing import List
from app import crud
from app.models import Colaborador, Servico

router = APIRouter()

# Colaborador Endpoints
@router.post("/colaboradores/", response_model=Colaborador)
def create_colaborador_endpoint(colaborador: Colaborador):
    return crud.create_colaborador(colaborador)

@router.get("/colaboradores/", response_model=List[Colaborador])
def read_colaboradores_endpoint():
    return crud.get_colaboradores()

@router.get("/colaboradores/{colaborador_id}", response_model=Colaborador)
def read_colaborador_endpoint(colaborador_id: int):
    db_colaborador = crud.get_colaborador_by_id(colaborador_id)
    if db_colaborador is None:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    return db_colaborador

@router.put("/colaboradores/{colaborador_id}", response_model=Colaborador)
def update_colaborador_endpoint(colaborador_id: int, colaborador: Colaborador):
    updated_colaborador = crud.update_colaborador(colaborador_id, colaborador)
    if updated_colaborador is None:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    return updated_colaborador

@router.delete("/colaboradores/{colaborador_id}", response_model=dict)
def delete_colaborador_endpoint(colaborador_id: int):
    result = crud.delete_colaborador(colaborador_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    return result

# Servico Endpoints
@router.post("/servicos/", response_model=Servico)
def create_servico_endpoint(servico: Servico):
    return crud.create_servico(servico)

@router.get("/servicos/", response_model=List[Servico])
def read_servicos_endpoint():
    return crud.get_servicos()

@router.get("/servicos/{servico_id}", response_model=Servico)
def read_servico_endpoint(servico_id: int):
    db_servico = crud.get_servico_by_id(servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Servico not found")
    return db_servico

@router.put("/servicos/{servico_id}", response_model=Servico)
def update_servico_endpoint(servico_id: int, servico: Servico):
    updated_servico = crud.update_servico(servico_id, servico)
    if updated_servico is None:
        raise HTTPException(status_code=404, detail="Servico not found")
    return updated_servico

@router.delete("/servicos/{servico_id}", response_model=dict)
def delete_servico_endpoint(servico_id: int):
    result = crud.delete_servico(servico_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Servico not found")
    return result