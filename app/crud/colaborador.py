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
            # Define effective end dates (using date.max for open-ended periods)
            new_end = colaborador.dataFim if colaborador.dataFim else date.max
            existing_end = existing.dataFim if existing.dataFim else date.max

            # Overlap check: (StartA <= EndB) and (EndA >= StartB)
            if colaborador.dataInicio <= existing_end and new_end >= existing.dataInicio:
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
        colaborador.dataInicio.isoformat(),
        colaborador.dataFim.isoformat() if colaborador.dataFim else ""
    ]
    sheet.append_row(row_data)
    return colaborador

def get_colaboradores() -> List[Colaborador]:
    sheet = get_colaboradores_sheet()
    records = sheet.get_all_records()
    colaboradores = []
    for record in records:
        # Handle potential empty strings for optional date fields
        record['dataFim'] = _parse_date(record.get('dataFim', ''))
        record['dataInicio'] = _parse_date(record.get('dataInicio', ''))
        # Basic data integrity check
        if record.get('id') and record.get('nome') and record.get('cpf') and record.get('percentualComissao') is not None:
            colaboradores.append(Colaborador(**record))
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
            new_end = colaborador.dataFim if colaborador.dataFim else date.max
            existing_end = existing.dataFim if existing.dataFim else date.max

            if colaborador.dataInicio <= existing_end and new_end >= existing.dataInicio:
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
        colaborador.dataInicio.isoformat(),
        colaborador.dataFim.isoformat() if colaborador.dataFim else ""
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