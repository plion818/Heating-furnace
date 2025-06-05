import streamlit as st
import pandas as pd

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    @st.cache_data
    def get_data(_self) -> pd.DataFrame: # Use _self because @st.cache_data injects the instance as the first arg
        """
        Loads data from the CSV file specified in self.file_path.
        Converts 'record Time' column to datetime objects.
        Returns:
            pd.DataFrame: The loaded and processed DataFrame.
        """
        try:
            df = pd.read_csv(_self.file_path)
            if 'record Time' in df.columns:
                df['record Time'] = pd.to_datetime(df['record Time'])
            else:
                # Handle cases where 'record Time' might be missing or named differently
                # For now, we can raise an error or return as is, depending on desired robustness
                st.error(f"Column 'record Time' not found in {_self.file_path}. Please ensure the CSV has this column.")
                # Or, depending on strictness: return df or raise ValueError
            return df
        except FileNotFoundError:
            st.error(f"File not found: {_self.file_path}. Please check the file path.")
            return pd.DataFrame() # Return empty DataFrame
        except Exception as e:
            st.error(f"An error occurred while loading data from {_self.file_path}: {e}")
            return pd.DataFrame() # Return empty DataFrame
