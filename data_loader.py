import streamlit as st
import pandas as pd
# No need to import UploadedFile from streamlit.uploaded_file_manager, type hinting is enough
from typing import Union, IO, AnyStr # For type hinting UploadedFile-like objects

class DataLoader:
    def __init__(self, source: Union[str, IO[AnyStr]]): # Accept string path or file-like object
        self.source = source

    @st.cache_data
    def get_data(_self) -> pd.DataFrame:
        """
        Loads data from the source (file path or uploaded file object).
        Converts 'record Time' column to datetime objects.
        Returns:
            pd.DataFrame: The loaded and processed DataFrame.
        """
        try:
            # pd.read_csv can handle file paths (str) and file-like objects (UploadedFile)
            df = pd.read_csv(_self.source)

            if 'record Time' in df.columns:
                df['record Time'] = pd.to_datetime(df['record Time'])
            else:
                # If 'record Time' is critical and missing, it's an issue.
                st.error(f"Column 'record Time' not found in the provided data. Please ensure the CSV has this column.")
                # Return empty DataFrame or raise error, depending on desired strictness.
                # For now, returning empty to let homepage handle it.
                return pd.DataFrame()
            return df
        except FileNotFoundError: # This error is specific to file paths
            st.error(f"File not found: {_self.source}. Please check the file path.")
            return pd.DataFrame()
        except pd.errors.EmptyDataError:
            st.error(f"The provided file is empty: {_self.source}.")
            return pd.DataFrame()
        except pd.errors.ParserError:
            st.error(f"Failed to parse the CSV file. Please ensure it is a valid CSV: {_self.source}.")
            return pd.DataFrame()
        except Exception as e:
            # General error catch for other issues (e.g., permissions if it's a path, unexpected errors)
            source_name = _self.source if isinstance(_self.source, str) else getattr(_self.source, 'name', 'uploaded file')
            st.error(f"An error occurred while loading data from {source_name}: {e}")
            return pd.DataFrame()
