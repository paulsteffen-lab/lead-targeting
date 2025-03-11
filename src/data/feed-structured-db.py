import pandas as pd
from loguru import logger
from sqlmodel import SQLModel, Session, create_engine, select
from src.config import settings
from src.data.models import LinkedinProfile

engine = create_engine(settings.structured_db_url, echo=True)


def main() -> None:
    """
    Execute the main process to create the database, preprocess data, and insert profiles.

    This function orchestrates the workflow by first creating the database and tables,
    then loading and preprocessing data from a pickle file, and finally inserting the
    preprocessed data as LinkedinProfile instances into the database. It logs a success
    message upon successful data insertion.

    Returns:
        None
    """
    create_db_and_tables()

    df = pd.read_pickle(settings.data_path / settings.data_filename)

    preprocessed_df = preprocess_data(df)

    create_profiles(preprocessed_df)

    logger.success(
        f"Data inserted successfully into the SQLite database at {engine.url} !"
    )


def create_db_and_tables() -> None:
    """
    Create the database and all associated tables.

    This function initializes the database schema by creating all tables
    defined in the SQLModel metadata using the specified database engine.
    """
    SQLModel.metadata.create_all(engine)


def create_profiles(df: pd.DataFrame) -> None:
    """
    Create and store LinkedinProfile instances in the database from a DataFrame.

    This function iterates over each row in the provided pandas DataFrame,
    creates a LinkedinProfile instance using the row data, and merge it to
    the database session. After processing all rows, the session is committed
    to persist the changes to the database.

    Args:
        df (pd.DataFrame): A DataFrame containing Linkedin profile data,
        where each row represents a profile with columns matching the
        LinkedinProfile model attributes.

    Returns:
        None
    """
    with Session(engine) as session:
        for _, row in df.iterrows():
            profile_dict = row.to_dict()
            existing_profile = _check_duplicates(session, profile_dict)

            if not existing_profile:
                profile = LinkedinProfile(**profile_dict)
                session.add(profile)
        session.commit()


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the input DataFrame by filtering and transforming its columns.

    This function filters the DataFrame to include only rows labeled as legitimate
    and removes specified useless columns. It then converts column names to lowercase
    and replaces spaces with underscores. Finally, it casts the DataFrame columns
    to the data types defined in the LinkedinProfile model.

    Parameters:
        df (pd.DataFrame): The input DataFrame to preprocess.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with filtered rows and transformed columns.
    """
    filtered_df = _filter_df(df)
    filtered_df.columns = _get_snake_case_columns(filtered_df.columns)
    preprocessed_df = _optimize_types(filtered_df)
    return preprocessed_df


def _check_duplicates(session: Session, profile_dict: dict) -> bool:
    """
    Check for duplicate LinkedinProfile entries in the database.

    Args:
        session (Session): The database session used to execute queries.
        profile_dict (dict): A dictionary containing 'full_name' and 'workplace' keys.

    Returns:
        bool: True if a duplicate profile exists, False otherwise.
    """
    full_name_filter = LinkedinProfile.full_name == profile_dict["full_name"]
    workplace_filter = LinkedinProfile.workplace == profile_dict["workplace"]

    existing_profile = session.exec(
        select(LinkedinProfile).filter(full_name_filter, workplace_filter)
    ).first()
    return True if existing_profile else False


def _filter_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter a DataFrame to remove non-legitimate entries and drop specific columns.

    This function filters the input DataFrame to retain only rows where the "Label"
    column is equal to 0, indicating legitimate entries. It also removes the "Label"
    and "Intro" columns from the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.

    Returns:
        pd.DataFrame: A filtered DataFrame with only legitimate entries and without
        the specified columns.
    """
    legitimate_mask = df["Label"] == 0
    useless_columns = ["Label", "Intro"]

    return df[legitimate_mask].drop(columns=useless_columns)


def _optimize_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize the data types of a DataFrame based on LinkedinProfile annotations.

    This function adjusts the data types of the columns in the given DataFrame
    to match the types defined in the LinkedinProfile model, for columns that
    exist in both the DataFrame and the model.

    Args:
        df (pd.DataFrame): The DataFrame whose column types are to be optimized.

    Returns:
        pd.DataFrame: A new DataFrame with optimized column data types.
    """
    dtypes = {
        k: v for k, v in LinkedinProfile.__annotations__.items() if k in df.columns
    }
    return df.astype(dtypes)


def _get_snake_case_columns(columns: pd.Series) -> list[str]:
    """
    Convert a Pandas Series of column names to snake_case.

    Parameters:
        columns (pd.Series): A Pandas Series containing column names.

    Returns:
        list[str]: A list of column names converted to snake_case.
    """
    return columns.str.lower().str.replace(" ", "_")


if __name__ == "__main__":
    main()
