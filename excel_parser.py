#excel_parser.py
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Union
import os

def parse_excel_or_csv(file_path: str, sheet_name: Union[str, int] = 0) -> List[Dict]:
    """
    Parses a CSV or Excel file and returns a cleaned list of dictionaries.

    Cleaning steps:
    - Converts NaN to None
    - Strips whitespace from string values
    - Converts known multiline fields to lists (e.g., TDM, SPR)

    Parameters:
        file_path (str): Path to the file
        sheet_name (str|int): Sheet name or index (Excel only)

    Returns:
        List[Dict]: Cleaned data rows
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if isinstance(file_path, Path):
        file_path = str(file_path)


    # Read the file
    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

    # Drop empty rows and columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Convert NaNs to None
    df = df.where(pd.notnull(df), None)

    # Strip whitespace from all strings
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert Timestamp to ISO string
    df = df.map(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, datetime)) else x)

    # Convert specific fields to lists if they contain newlines
    multiline_fields = ["TDM", "SPR"]
    for field in multiline_fields:
        if field in df.columns:
            df[field] = df[field].apply(lambda x: x.split("\n") if isinstance(x, str) and "\n" in x else x)

    return df.to_dict(orient="records")
