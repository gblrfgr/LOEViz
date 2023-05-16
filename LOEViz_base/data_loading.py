import pandas as pd
import typing
import logging
import sys


def validate_columns(df: pd.DataFrame):
    """
    Validates that the spreadsheet has the correct column titles. Logs an
    error and exits if the column titles are incorrect; the error is
    unrecoverable.

    Args:
        df (pd.DataFrame): The loaded-in spreadsheet.
    """
    EXPECTED = pd.Index(
        ["ID", "Description", "Start Date", "End Date", "Status", "Dependencies"]
    )
    if len(df.columns) != len(EXPECTED) or df.columns != EXPECTED:
        for actual in df.columns:
            if actual not in EXPECTED:
                logging.error(f'Unexpected column "{actual}"')
        for title in EXPECTED:
            if title not in df.columns:
                logging.error(f'Expected but did not find column "{title}"')
        logging.error("Invalid columns, rejecting data")
        logging.warn("Columns must not be modified from the template")
        sys.exit(-1)


def load_data(filename: str) -> pd.DataFrame:
    """Load project data from an Excel worksheet.

    Args:
        filename (str): The path to the worksheet.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the project data.
    """
    try:
        df = pd.read_excel(filename)
    except FileNotFoundError as e:
        logging.error(f'Did not find file "{filename}"')
        sys.exit(-1)
    except e:
        logging.error(f'Encountered unexpected error "{e.strerror}"')
        sys.exit(-1)
    validate_columns(df)
    return df
