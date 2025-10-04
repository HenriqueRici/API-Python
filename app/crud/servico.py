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
            # Define effective end dates (using date.max for open-ended services)
            new_end = servico.dataFim if servico.dataFim else date.max
            existing_end = existing_servico.dataFim if existing_servico.dataFim else date.max

            # Overlap check: (StartA <= EndB) and (EndA >= StartB)
            if servico.dataInicio <= existing_end and new_end >= existing_servico.dataInicio:
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
        servico.dataFim.isoformat() if servico.dataFim else ""
    ]
    sheet.append_row(row_data)
    return servico

def get_servicos() -> List[Servico]:
    sheet = get_servicos_sheet()
    records = sheet.get_all_records()
    servicos = []
    for record in records:
        record['dataFim'] = _parse_date(record.get('dataFim', ''))
        record['dataInicio'] = _parse_date(record.get('dataInicio', ''))
        if record.get('id') and record.get('tipoServico'): # Basic data integrity check
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
        if existing.tipoServico == servico.tipoServico and existing.id != servico_id:
            new_end = servico.dataFim if servico.dataFim else date.max
            existing_end = existing.dataFim if existing.dataFim else date.max
            if servico.dataInicio <= existing_end and new_end >= existing.dataInicio:
                 raise ValueError(f"A atualização causa sobreposição de datas para o serviço '{servico.tipoServico}'.")

    row_number = cell.row
    servico.id = servico_id
    row_data = [
        str(servico.id),
        servico.tipoServico,
        str(servico.valor),
        servico.dataInicio.isoformat(),
        servico.dataFim.isoformat() if servico.dataFim else ""
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