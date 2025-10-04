import gspread
from typing import Optional
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