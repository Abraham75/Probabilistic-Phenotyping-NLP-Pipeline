# db_reader.py
import logging
from typing import List, Dict, Optional
import pandas as pd
import os

class DbReader:
    """
    Robust EHR database reader for free-text and structured clinical data.

    Reads and validates EHR sources (notes, medications, diagnoses, labs)
    from CSV files, providing structured access for modeling pipelines.

    Attributes:
        notes_path (str): Path to free-text clinical notes CSV.
        meds_path (str): Path to medications table CSV.
        diag_path (str): Path to diagnosis codes CSV.
        labs_path (str): Path to laboratory results CSV.
    """

    def __init__(
        self, 
        notes_path: str, 
        meds_path: str, 
        diag_path: str, 
        labs_path: str,
        csv_options: Optional[Dict] = None
    ):
        """
        Initializes DbReader with file paths and optional CSV arguments.

        Args:
            notes_path (str): Path to notes CSV file.
            meds_path (str): Path to medications CSV file.
            diag_path (str): Path to diagnoses CSV file.
            labs_path (str): Path to labs CSV file.
            csv_options (Optional[Dict]): Extra options passed to pd.read_csv.
        """
        self.notes_path = notes_path
        self.meds_path = meds_path
        self.diag_path = diag_path
        self.labs_path = labs_path
        self.csv_options = csv_options or {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        for path in [notes_path, meds_path, diag_path, labs_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")

    def read_notes(self) -> List[Dict]:
        """
        Loads free-text notes from the CSV file.

        Returns:
            List[Dict]: List of dicts ({'patient_id': ..., 'note_text': ...})

        Raises:
            ValueError: If required columns are missing.
        """
        df = pd.read_csv(self.notes_path, **self.csv_options)
        required = {'patient_id', 'note_text'}
        if not required.issubset(df.columns):
            missing = required - set(df.columns)
            raise ValueError(f"Missing columns in notes file: {missing}")
        self.logger.info("Read %d notes from %s", len(df), self.notes_path)
        return df.to_dict(orient='records')

    def read_structured(self) -> Dict[str, pd.DataFrame]:
        """
        Loads structured tables for medications, diagnoses, and labs.

        Returns:
            Dict[str, pd.DataFrame]: Keys are 'meds', 'diag', 'labs'.
        
        Raises:
            ValueError: If any CSV is corrupted or missing expected columns.
        """
        result = {}
        # Medications
        meds = pd.read_csv(self.meds_path, **self.csv_options)
        if 'patient_id' not in meds.columns:
            raise ValueError("Missing required column 'patient_id' in medications file.")
        result['meds'] = meds
        # Diagnoses
        diag = pd.read_csv(self.diag_path, **self.csv_options)
        if 'patient_id' not in diag.columns:
            raise ValueError("Missing required column 'patient_id' in diagnoses file.")
        result['diag'] = diag
        # Labs
        labs = pd.read_csv(self.labs_path, **self.csv_options)
        if 'patient_id' not in labs.columns:
            raise ValueError("Missing required column 'patient_id' in labs file.")
        result['labs'] = labs

        self.logger.info(
            "Loaded data: meds (%d rows), diag (%d rows), labs (%d rows)",
            len(meds), len(diag), len(labs)
        )
        return result
