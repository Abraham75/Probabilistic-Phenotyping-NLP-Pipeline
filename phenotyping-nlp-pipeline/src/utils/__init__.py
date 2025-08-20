# init__.py
# __init__.py

"""
Clinical Phenotyping Pipeline Package
=====================================

This package provides an end-to-end probabilistic phenotyping pipeline from
heterogeneous Electronic Health Record (EHR) data, including free-text notes
and structured clinical information.

Modules:
- db_reader: EHR data ingestion and validation
- nlp_pipeline: Clinical NLP processing using spaCy
- valence_detector: Valence scoring of clinical concepts
- phenotyping_engine: Domain-informed clinical phenotyping and probabilistic modeling
- db_writer: Output generation of phenotype summaries

Example usage:
--------------
from phenotyping_pipeline import ClinicalPhenotypingPipeline

pipeline = ClinicalPhenotypingPipeline(config)
pipeline.run()
"""

__version__ = "1.0.0"

# Import core classes for easy access at the package level
from .db_reader import DbReader
from .nlp_pipeline import NLPProcessor
# Assuming additional modules exist; placeholders for demonstration:
# from .valence_detector import ValenceDetector
# from .phenotyping_engine import PhenotypingEngine
# from .db_writer import DbWriter
from .pipeline import ClinicalPhenotypingPipeline  # Or main orchestration class

# Define __all__ for explicit exports
__all__ = [
    "DbReader",
    "NLPProcessor",
    # "ValenceDetector",
    # "PhenotypingEngine",
    # "DbWriter",
    "ClinicalPhenotypingPipeline",
]

