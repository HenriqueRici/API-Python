from app.database import get_colaboradores_sheet, get_servicos_sheet
from app.models import Colaborador, Servico
from typing import List, Optional
import gspread
from datetime import date, datetime

def get_next_id(sheet: gspread.Worksheet) -> int:
    """Gets the next available ID from a worksheet."""
    all_values = sheet.get_all_values()
    if len(all_values) <= 1:
        return 1
    # Filter for rows where the first cell is a digit, then convert to int
    ids = [int(row[0]) for row in all_values[1:] if row and row[0].isdigit()]
    return max(ids) + 1 if ids else 1

def _parse_date(date_str: str) -> Optional[date]:
    """Helper to parse date strings from sheet, returning None if empty."""
    if not date_str:
        return None
    try:
        # Assumes date is in ISO format YYYY-MM-DD
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

# Colaborador CRUD
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

# Servico CRUD
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