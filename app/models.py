from pydantic import BaseModel
from typing import Optional
from datetime import date

class Colaborador(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    chavePix: str
    dataInicio: date
    dataFim: Optional[date] = None

class Servico(BaseModel):
    id: Optional[int] = None
    tipoServico: str
    valor: float
    dataInicio: date
    dataFim: Optional[date] = None