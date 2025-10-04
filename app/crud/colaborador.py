from app.database import get_colaboradores_sheet
from app.models import Colaborador
from typing import List, Optional
from datetime import date
from app.crud.utils import get_next_id, _parse_date

def create_colaborador(colaborador: Colaborador) -> Colaborador:
    sheet = get_colaboradores_sheet()
    all_colaboradores = get_colaboradores()

    # Check for existing CPF with overlapping dates
    for existing in all_colaboradores:
        if existing.cpf == colaborador.cpf:
            # Overlap check: (StartA <= EndB) and (EndA >= StartB)
            if colaborador.dataInicio <= existing.dataFim and colaborador.dataFim >= existing.dataInicio:
                raise ValueError(
                    f"Colaborador com CPF {colaborador.cpf} já possui um cadastro ativo no período informado."
                )

    next_id = get_next_id(sheet)
    colaborador.id = next_id
    # Convert model data to a list of strings for the sheet
    row_data = [
        str(colaborador.id),
        colaborador.nome,
        colaborador.cpf,
        colaborador.chavePix,
        str(colaborador.percentualComissao),
        colaborador.dataInicio.strftime('%d/%m/%Y'),
        colaborador.dataFim.strftime('%d/%m/%Y')
    ]
    sheet.append_row(row_data)
    return colaborador

def get_colaboradores() -> List[Colaborador]:
    sheet = get_colaboradores_sheet()
    records = sheet.get_all_records()
    colaboradores = []
    for record in records:
        try:
            # Build a dictionary with correct types for Pydantic model creation.
            data_to_validate = {
                'id': int(record['id']),
                'nome': record['nome'],
                'cpf': record['cpf'],
                'chavePix': record['chavePix'],
                'percentualComissao': float(record['percentualComissao']),
                'dataInicio': _parse_date(record.get('dataInicio')),
                'dataFim': _parse_date(record.get('dataFim')),
            }

            # After parsing, ensure date fields (now mandatory) are not None before creating the model.
            if not data_to_validate['dataInicio'] or not data_to_validate['dataFim']:
                continue

            colaboradores.append(Colaborador(**data_to_validate))
        except (ValueError, TypeError, KeyError):
            # If any required field is missing or has a wrong type,
            # safely skip this row and continue processing others.
            continue
    return colaboradores

def get_colaborador_by_id(colaborador_id: int) -> Optional[Colaborador]:
    all_colaboradores = get_colaboradores()
    for colaborador in all_colaboradores:
        if colaborador.id == colaborador_id:
            return colaborador
    return None

def update_colaborador(colaborador_id: int, colaborador: Colaborador) -> Optional[Colaborador]:
    sheet = get_colaboradores_sheet()
    cell = sheet.find(str(colaborador_id))
    if not cell:
        return None

    all_colaboradores = get_colaboradores()
    for existing in all_colaboradores:
        # Check for conflicts with *other* collaborators
        if existing.cpf == colaborador.cpf and existing.id != colaborador_id:
            if colaborador.dataInicio <= existing.dataFim and colaborador.dataFim >= existing.dataInicio:
                raise ValueError(
                    f"A atualização conflita com um cadastro existente para o CPF {colaborador.cpf} no período informado."
                )

    row_number = cell.row
    colaborador.id = colaborador_id
    row_data = [
        str(colaborador.id),
        colaborador.nome,
        colaborador.cpf,
        colaborador.chavePix,
        str(colaborador.percentualComissao),
        colaborador.dataInicio.strftime('%d/%m/%Y'),
        colaborador.dataFim.strftime('%d/%m/%Y')
    ]
    sheet.update(f'A{row_number}:G{row_number}', [row_data])
    return colaborador

def delete_colaborador(colaborador_id: int) -> Optional[dict]:
    sheet = get_colaboradores_sheet()
    cell = sheet.find(str(colaborador_id))
    if not cell:
        return None
    sheet.delete_rows(cell.row)
    return {"message": "Colaborador deleted successfully"}