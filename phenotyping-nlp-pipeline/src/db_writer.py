#db_writer.py
# db_writer.py

import pandas as pd
import os
import logging
from typing import List, Dict, Optional, Union

class DbWriter:
    """
    Responsible for writing structured phenotype summaries to persistent storage.
    Supports CSV and optionally other formats for extensibility.

    Attributes:
        output_path (str): File path where output will be saved.
        file_format (str): File format for output (default 'csv').
        index (bool): Whether to write row indices (default False).
        overwrite (bool): Overwrite existing files (default True).
    """

    def __init__(
        self,
        output_path: str,
        file_format: str = "csv",
        index: bool = False,
        overwrite: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        self.output_path = output_path
        self.file_format = file_format.lower()
        self.index = index
        self.overwrite = overwrite

        if logger is None:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self._validate_output_path()

    def _validate_output_path(self):
        """
        Validates the output path and directory existence.
        Creates directories if they do not exist.
        Raises error if directory cannot be created.
        """
        directory = os.path.dirname(self.output_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"Created output directory {directory}")
            except Exception as e:
                self.logger.error(f"Failed to create directory {directory}: {e}")
                raise

        if not self.overwrite and os.path.exists(self.output_path):
            msg = f"Output file {self.output_path} exists and overwrite is disabled."
            self.logger.error(msg)
            raise FileExistsError(msg)

    def write(self, data: List[Dict[str, Union[str, float, int]]]) -> None:
        """
        Write phenotype summaries to file.

        Args:
            data (List[Dict]): List of phenotype dicts, e.g. [{'patient_id': ..., 'INFECTION': 0.7, ...}, ...].

        Raises:
            ValueError: If data is empty or invalid format.
            IOError: If file writing fails.
        """
        if not data:
            raise ValueError("No data provided for writing.")

        try:
            df = pd.DataFrame(data)
            if df.empty:
                raise ValueError("DataFrame is empty after conversion from data.")

            if self.file_format == "csv":
                df.to_csv(self.output_path, index=self.index)
                self.logger.info(f"Wrote {len(df)} records to CSV: {self.output_path}")
            else:
                self.logger.warning(f"Unsupported file format '{self.file_format}'. No data written.")
                raise NotImplementedError(f"File format '{self.file_format}' is not supported.")

        except Exception as e:
            self.logger.error(f"Failed to write data to {self.output_path}: {e}")
            raise


# Example usage (can be removed or placed under a test script):
if __name__ == "__main__":
    data = [
        {'patient_id': '123', 'INFECTION': 0.85, 'DIABETES': 0.1},
        {'patient_id': '456', 'INFECTION': 0.15, 'DIABETES': 0.95},
    ]
    writer = DbWriter(output_path="output/phenotypes.csv")
    writer.write(data)
