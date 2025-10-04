from app.database import get_colaboradores_sheet, get_servicos_sheet
from app.models import Colaborador, Servico
from typing import List, Optional
import gspread

def get_next_id(sheet: gspread.Worksheet) -> int:
    """Gets the next available ID from a worksheet."""
    all_values = sheet.get_all_values()
    if len(all_values) <= 1:
        return 1
    ids = [int(row[0]) for row in all_values[1:] if row[0].isdigit()]
    return max(ids) + 1 if ids else 1

# Colaborador CRUD
def create_colaborador(colaborador: Colaborador) -> Colaborador:
    sheet = get_colaboradores_sheet()
    next_id = get_next_id(sheet)
    colaborador.id = next_id
    sheet.append_row(list(colaborador.dict().values()))
    return colaborador

def get_colaboradores() -> List[Colaborador]:
    sheet = get_colaboradores_sheet()
    records = sheet.get_all_records()
    return [Colaborador(**record) for record in records]

def get_colaborador_by_id(colaborador_id: int) -> Optional[Colaborador]:
    sheet = get_colaboradores_sheet()
    records = sheet.get_all_records()
    for record in records:
        if record.get("id") == colaborador_id:
            return Colaborador(**record)
    return None

def update_colaborador(colaborador_id: int, colaborador: Colaborador) -> Optional[Colaborador]:
    sheet = get_colaboradores_sheet()
    cell = sheet.find(str(colaborador_id))
    if not cell:
        return None
    row_number = cell.row
    colaborador.id = colaborador_id
    sheet.update(f'A{row_number}:F{row_number}', [list(colaborador.dict().values())])
    return colaborador

def delete_colaborador(colaborador_id: int) -> Optional[dict]:
    sheet = get_colaboradores_sheet()
    cell = sheet.find(str(colaborador_id))
    if not cell:
        return None
    sheet.delete_rows(cell.row)
    return {"message": "Colaborador deleted successfully"}

# Servico CRUD
def create_servico(servico: Servico) -> Servico:
    sheet = get_servicos_sheet()
    next_id = get_next_id(sheet)
    servico.id = next_id
    sheet.append_row(list(servico.dict().values()))
    return servico

def get_servicos() -> List[Servico]:
    sheet = get_servicos_sheet()
    records = sheet.get_all_records()
    return [Servico(**record) for record in records]

def get_servico_by_id(servico_id: int) -> Optional[Servico]:
    sheet = get_servicos_sheet()
    records = sheet.get_all_records()
    for record in records:
        if record.get("id") == servico_id:
            return Servico(**record)
    return None

def update_servico(servico_id: int, servico: Servico) -> Optional[Servico]:
    sheet = get_servicos_sheet()
    cell = sheet.find(str(servico_id))
    if not cell:
        return None
    row_number = cell.row
    servico.id = servico_id
    sheet.update(f'A{row_number}:E{row_number}', [list(servico.dict().values())])
    return servico

def delete_servico(servico_id: int) -> Optional[dict]:
    sheet = get_servicos_sheet()
    cell = sheet.find(str(servico_id))
    if not cell:
        return None
    sheet.delete_rows(cell.row)
    return {"message": "Servico deleted successfully"}