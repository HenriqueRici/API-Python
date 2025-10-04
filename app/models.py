from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class Colaborador(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    chavePix: str
    percentualComissao: float
    dataInicio: date
    dataFim: date

    @validator('dataFim')
    def validate_data_fim(cls, v, values):
        if 'dataInicio' in values and v < values['dataInicio']:
            raise ValueError('A data de fim não pode ser anterior à data de início.')
        return v

class Servico(BaseModel):
    id: Optional[int] = None
    tipoServico: str
    valor: float
    dataInicio: date
    dataFim: date

    @validator('dataFim')
    def validate_data_fim(cls, v, values):
        if 'dataInicio' in values and v < values['dataInicio']:
            raise ValueError('A data de fim não pode ser anterior à data de início.')
        return v