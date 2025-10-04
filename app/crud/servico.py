from app.database import get_servicos_sheet
from app.models import Servico
from typing import List, Optional
from datetime import date
from app.crud.utils import get_next_id, _parse_date

def create_servico(servico: Servico) -> Servico:
    sheet = get_servicos_sheet()
    all_servicos = get_servicos()

    # Check for overlapping services of the same type
    for existing_servico in all_servicos:
        if existing_servico.tipoServico == servico.tipoServico:
            # Overlap check: (StartA <= EndB) and (EndA >= StartB)
            if servico.dataInicio <= existing_servico.dataFim and servico.dataFim >= existing_servico.dataInicio:
                raise ValueError(
                    f"Serviço do tipo '{servico.tipoServico}' já existe em um período sobreposto."
                )

    next_id = get_next_id(sheet)
    servico.id = next_id
    row_data = [
        str(servico.id),
        servico.tipoServico,
        str(servico.valor),
        servico.dataInicio.isoformat(),
        servico.dataFim.isoformat()
    ]
    sheet.append_row(row_data)
    return servico

def get_servicos() -> List[Servico]:
    sheet = get_servicos_sheet()
    records = sheet.get_all_records()
    servicos = []
    for record in records:
        record['dataInicio'] = _parse_date(record.get('dataInicio', ''))
        record['dataFim'] = _parse_date(record.get('dataFim', ''))
        # Basic data integrity check, ensure required fields are present
        if all(record.get(key) for key in ['id', 'tipoServico', 'valor', 'dataInicio', 'dataFim']):
            servicos.append(Servico(**record))
    return servicos

def get_servico_by_id(servico_id: int) -> Optional[Servico]:
    all_servicos = get_servicos()
    for servico in all_servicos:
        if servico.id == servico_id:
            return servico
    return None

def update_servico(servico_id: int, servico: Servico) -> Optional[Servico]:
    sheet = get_servicos_sheet()
    cell = sheet.find(str(servico_id))
    if not cell:
        return None

    all_servicos = get_servicos()
    for existing in all_servicos:
        # Check for conflicts with *other* services
        if existing.tipoServico == servico.tipoServico and existing.id != servico_id:
            if servico.dataInicio <= existing.dataFim and servico.dataFim >= existing.dataInicio:
                 raise ValueError(f"A atualização causa sobreposição de datas para o serviço '{servico.tipoServico}'.")

    row_number = cell.row
    servico.id = servico_id
    row_data = [
        str(servico.id),
        servico.tipoServico,
        str(servico.valor),
        servico.dataInicio.isoformat(),
        servico.dataFim.isoformat()
    ]
    sheet.update(f'A{row_number}:E{row_number}', [row_data])
    return servico

def delete_servico(servico_id: int) -> Optional[dict]:
    sheet = get_servicos_sheet()
    cell = sheet.find(str(servico_id))
    if not cell:
        return None
    sheet.delete_rows(cell.row)
    return {"message": "Servico deleted successfully"}