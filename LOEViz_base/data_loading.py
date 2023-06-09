import pandas as pd
import typing
import logging
import sys
import re


def validate_columns(df: pd.DataFrame):
    """
    Validates that the spreadsheet has the correct column titles. Logs an error and
    exits if the column titles are incorrect; the error is unrecoverable.

    Args:
        df (pd.DataFrame): The loaded-in spreadsheet.
    """
    EXPECTED = pd.Index(
        ["ID", "Description", "Start Date", "End Date", "Status", "Dependencies"]
    )
    if (len(df.columns) != len(EXPECTED)) or (df.columns != EXPECTED).any():
        for actual in df.columns:
            if actual not in EXPECTED:
                logging.error(f'Unexpected column "{actual}"')
        for title in EXPECTED:
            if title not in df.columns:
                logging.error(f'Expected but did not find column "{title}"')
        logging.error("Invalid columns, rejecting data")
        logging.warn("Columns must not be modified from the template")
        sys.exit(-1)


def validate_ids(df: pd.DataFrame):
    """Validates that all IDs are in the correct format and unique.

    Args:
        df (pd.DataFrame): The DataFrame containing the project data.
    """
    for actual in df["ID"]:
        actual = actual.lower()
        if not (
            re.fullmatch(r"loe[1-9]+", actual) is not None
            or re.fullmatch(r"o[1-9]+\.[1-9]+", actual) is not None
            or re.fullmatch(r"io[1-9]+\.[1-9]+\.[1-9]+", actual) is not None
        ):
            logging.error(f'Invalid ID "{actual}", rejecting data')
            sys.exit(-1)
    uniques = set()
    for actual in df["ID"]:
        actual = actual.lower()
        if actual in uniques:
            logging.error(f'Duplicate ID "{actual}", rejecting data')
            sys.exit(-1)
        uniques.add(actual)


def validate_dates(df: pd.DataFrame):
    """Validates that all start and end dates are in the correct format and order.

    Args:
        df (pd.DataFrame): The DataFrame containing the project data.
    """
    for start, end in zip(df["Start Date"], df["End Date"]):
        if not isinstance(start, pd.Timestamp):
            logging.error(f'Invalid date data "{start}"')
            sys.exit(-1)
        elif not isinstance(end, pd.Timestamp):
            logging.error(f'Invalid date data "{end}"')
            sys.exit(-1)
        elif start >= end:
            logging.error(f'Goal start date "{start}" is on or after end date "{end}"')
            sys.exit(-1)


def validate_statuses(df: pd.DataFrame):
    """Validate that all project statuses are in the expected set.

    Args:
        df (pd.DataFrame): The DataFrame containing the project data.
    """
    EXPECTED = {"overdue", "at risk", "on track", "complete"}
    for status in df["Status"]:
        status = status.lower()
        if status not in EXPECTED:
            logging.error(f'Invalid project status "{status}"')
            sys.exit(-1)


def validate_dependencies(df: pd.DataFrame):
    """Validate that all project dependencies are in the correct format and exist.

    Args:
        df (pd.DataFrame): The DataFrame containing the project data.
    """
    for dependency_list in df["Dependencies"]:
        if not isinstance(dependency_list, str):
            continue
        dependencies = dependency_list.split(",")
        for dependency in dependencies:
            if not (df["ID"] == dependency).any():
                logging.error(f"Invalid dependencies \"{','.join(dependencies)}\"")
                sys.exit(-1)


def process_statuses(df: pd.DataFrame) -> pd.DataFrame:
    """Update the statuses of each different task in a project to reflect the current
    overall state.

    Args:
        df (pd.DataFrame): The DataFrame containing the project data.

    Returns:
        pd.DataFrame: A new DataFrame containing the updated project data.
    """
    overdue_updated = df.copy()
    for ind, row in df.iterrows():
        if (
            row["End Date"] < pd.Timestamp.today()
            and row["Status"].lower() != "complete"
        ):
            row["Status"] = "Overdue"
        overdue_updated.loc[ind] = row
    dependency_updated = overdue_updated.copy()
    for ind, row in overdue_updated.iterrows():
        dependency_list = row["Dependencies"]
        if not isinstance(dependency_list, str):
            continue
        dependencies = dependency_list.split(",")
        for dep in dependencies:
            dep_ind = overdue_updated.index[overdue_updated["ID"] == dep].to_list()[0]
            dep_row = overdue_updated.loc[dep_ind]
            if (
                dep_row["Status"].lower() == "overdue"
                and row["Status"].lower() != "overdue"
            ):
                dependency_updated.at[ind, "Status"] = "At Risk"
    return dependency_updated


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
    validate_ids(df)
    validate_dates(df)
    validate_statuses(df)
    validate_dependencies(df)
    result = process_statuses(df)
    result.to_excel(filename, sheet_name="LOEs, IOs, and Objectives", index=False)
    return result
