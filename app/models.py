from pydantic import BaseModel, validator
from typing import Optional, Any
from datetime import date, datetime

class Colaborador(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    chavePix: str
    percentualComissao: float
    dataInicio: date
    dataFim: date

    @validator('dataInicio', 'dataFim', pre=True, allow_reuse=True)
    def parse_date_br_format(cls, v: Any) -> date:
        """Allow date inputs in DD/MM/YYYY format."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                raise ValueError(f"Formato de data inválido: '{v}'. Use DD/MM/YYYY.")
        return v

    @validator('dataFim', allow_reuse=True)
    def validate_data_fim_after_data_inicio(cls, v: date, values: dict) -> date:
        """Ensure end date is not before start date."""
        if 'dataInicio' in values and values.get('dataInicio') and v < values['dataInicio']:
            raise ValueError('A data de fim não pode ser anterior à data de início.')
        return v

class Servico(BaseModel):
    id: Optional[int] = None
    tipoServico: str
    valor: float
    dataInicio: date
    dataFim: date

    @validator('dataInicio', 'dataFim', pre=True, allow_reuse=True)
    def parse_date_br_format(cls, v: Any) -> date:
        """Allow date inputs in DD/MM/YYYY format."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                raise ValueError(f"Formato de data inválido: '{v}'. Use DD/MM/YYYY.")
        return v

    @validator('dataFim', allow_reuse=True)
    def validate_data_fim_after_data_inicio(cls, v: date, values: dict) -> date:
        """Ensure end date is not before start date."""
        if 'dataInicio' in values and values.get('dataInicio') and v < values['dataInicio']:
            raise ValueError('A data de fim não pode ser anterior à data de início.')
        return v