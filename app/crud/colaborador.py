from app.database import get_colaboradores_sheet
from app.models import Colaborador
from typing import List, Optional
from datetime import date
from app.crud.utils import get_next_id, _parse_date

def create_colaborador(colaborador: Colaborador) -> Colaborador:
    sheet = get_colaboradores_sheet()

    # Check for existing CPF
    all_colaboradores = get_colaboradores()
    for existing in all_colaboradores:
        if existing.cpf == colaborador.cpf:
            raise ValueError(f"Colaborador com CPF {colaborador.cpf} já existe.")

    next_id = get_next_id(sheet)
    colaborador.id = next_id
    # Convert model data to a list of strings for the sheet
    row_data = [
        str(colaborador.id),
        colaborador.nome,
        colaborador.cpf,
        colaborador.chavePix,
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
        if record.get('id') and record.get('nome') and record.get('cpf'): # Basic data integrity check
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
        if existing.cpf == colaborador.cpf and existing.id != colaborador_id:
            raise ValueError(f"Outro colaborador já possui o CPF {colaborador.cpf}.")

    row_number = cell.row
    colaborador.id = colaborador_id
    row_data = [
        str(colaborador.id),
        colaborador.nome,
        colaborador.cpf,
        colaborador.chavePix,
        colaborador.dataInicio.isoformat(),
        colaborador.dataFim.isoformat() if colaborador.dataFim else ""
    ]
    sheet.update(f'A{row_number}:F{row_number}', [row_data])
    return colaborador

def delete_colaborador(colaborador_id: int) -> Optional[dict]:
    sheet = get_colaboradores_sheet()
    cell = sheet.find(str(colaborador_id))
    if not cell:
        return None
    sheet.delete_rows(cell.row)
    return {"message": "Colaborador deleted successfully"}