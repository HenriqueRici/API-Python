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
        servico.dataInicio.strftime('%d/%m/%Y'),
        servico.dataFim.strftime('%d/%m/%Y')
    ]
    sheet.append_row(row_data)
    return servico

def get_servicos() -> List[Servico]:
    sheet = get_servicos_sheet()
    records = sheet.get_all_records()
    servicos = []
    for record in records:
        try:
            # Build a dictionary with correct types for Pydantic model creation.
            data_to_validate = {
                'id': int(record['id']),
                'tipoServico': record['tipoServico'],
                'valor': float(record['valor']),
                'dataInicio': _parse_date(record.get('dataInicio')),
                'dataFim': _parse_date(record.get('dataFim')),
            }

            # After parsing, ensure date fields (now mandatory) are not None.
            if not data_to_validate['dataInicio'] or not data_to_validate['dataFim']:
                continue

            servicos.append(Servico(**data_to_validate))
        except (ValueError, TypeError, KeyError):
            # If any required field is missing or has a wrong type,
            # safely skip this row and continue processing others.
            continue
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
        servico.dataInicio.strftime('%d/%m/%Y'),
        servico.dataFim.strftime('%d/%m/%Y')
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