#phenotyping_module.py
Below is a **modular Python code template** for an end-to-end clinical NLP pipeline for **probabilistic phenotyping** from heterogeneous EHR data. Each component is organized into classes and functions, aligned with the architecture and requirements you described. Some functions include realistic stubs for plug-and-play of actual logic, making the workflow easy to extend and adapt for research-grade development. 

This code is heavily commented to serve as a template for a PHT-level project, drawing from the referenced UPhenome approach.

***

```python
# clinical_phenotyping_pipeline.py

import os
from typing import List, Dict, Any
import spacy
from spacy.tokens import Doc
from collections import defaultdict
import pandas as pd
import numpy as np

# 1. DbReader: Reads raw EHR text and structured files
class DbReader:
    def __init__(self, notes_path, meds_path, diag_path, labs_path):
        self.notes_path = notes_path
        self.meds_path = meds_path
        self.diag_path = diag_path
        self.labs_path = labs_path

    def read_notes(self) -> List[Dict]:
        # Stub: read free-text notes from file(s)
        df = pd.read_csv(self.notes_path)
        # Expects columns: ['patient_id', 'note_text']
        return df.to_dict('records')

    def read_structured(self) -> Dict[str, pd.DataFrame]:
        # Returns structured dataframes: medications, diagnoses, labs
        meds = pd.read_csv(self.meds_path)
        diag = pd.read_csv(self.diag_path)
        labs = pd.read_csv(self.labs_path)
        return {'meds': meds, 'diag': diag, 'labs': labs}

# 2. spaCy NLP: Tokenizes, sections, contextualizes input
class NLPProcessor:
    def __init__(self, model='en_core_sci_sm'):
        self.nlp = spacy.load(model)

    def process_note(self, note_text: str) -> Doc:
        doc = self.nlp(note_text)
        return doc # Sentences, tokens, entities, etc.

# 3. Valence Detector: Labels n-gram positivity/negativity
class ValenceDetector:
    def __init__(self, valence_lexicon: Dict[str, int]):
        self.lexicon = valence_lexicon # e.g., {'fever': 1, 'no fever': -1}

    def detect(self, doc: Doc) -> Dict[str, int]:
        results = {}
        for ent in doc.ents:
            key = ent.text.lower()
            results[key] = self.lexicon.get(key, 0)
        return results

# 4. Phenotyping Engine: Tags tokens into clinically-related groups (domain-informed)
class PhenotypingEngine:
    def __init__(self, phenotyping_rules: Dict[str, List[str]]):
        self.rules = phenotyping_rules  # e.g., { "INFECTION": ["fever", "cough", ...] }

    def tag(self, detected_tokens: Dict[str, int]) -> Dict[str, float]:
        grouped = defaultdict(list)
        for group, keywords in self.rules.items():
            for kw in keywords:
                if kw in detected_tokens:
                    grouped[group].append(detected_tokens[kw])
        # Simple probabilistic: sum counts, normalize (placeholder for logistic/Bayesian model)
        output = {}
        for group, vals in grouped.items():
            if vals:
                # Probabilistic example: mean valence as phenotype probability
                output[group] = (np.mean(vals) + 1)/2 # Map from [-1,1] to [0,1]
            else:
                output[group] = 0.0
        return output

# 5. DbWriter: Outputs structured phenotype summaries
class DbWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, phenotypes: List[Dict]): 
        df = pd.DataFrame(phenotypes)
        df.to_csv(self.output_path, index=False)

# Pipeline Orchestrator
class ClinicalPhenotypingPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.reader = DbReader(config['notes'], config['meds'], config['diag'], config['labs'])
        self.nlp = NLPProcessor()
        self.valence = ValenceDetector(config['valence_lexicon'])
        self.pheno = PhenotypingEngine(config['phenotyping_rules'])
        self.writer = DbWriter(config['output'])

    def run(self):
        notes = self.reader.read_notes()
        structured = self.reader.read_structured()
        phenotype_summaries = []
        for note in notes:
            doc = self.nlp.process_note(note['note_text'])
            detections = self.valence.detect(doc)
            pheno_scores = self.pheno.tag(detections)
            phenotype_summaries.append({'patient_id': note['patient_id'], **pheno_scores})
        self.writer.write(phenotype_summaries)
        print("Phenotype extraction complete.")

# ========= USAGE ===========
if __name__ == '__main__':
    # Example example config
    config = {
        'notes': 'ehr_notes.csv',
        'meds': 'ehr_meds.csv',
        'diag': 'ehr_diagnosis.csv',
        'labs': 'ehr_labs.csv',
        'valence_lexicon': {
            'fever': 1,
            'no fever': -1,
            'cough': 1,
            'no cough': -1
            # ... expand for your domain
        },
        'phenotyping_rules': {
            'INFECTION': ['fever', 'cough'],
            # ... expand groupings
        },
        'output': 'phenotype_summary.csv'
    }

    pipeline = ClinicalPhenotypingPipeline(config)
    pipeline.run()
```

***

### Notes
- **spaCy** model selection: Use a clinical model (e.g., scispaCy or custom-trained) for best results in production.
- **Valence Detection and Probabilistic Modeling**: Substitute in advanced logic/Bayesian modeling as per your research or as per UPhenome's LDA-inspired mechanisms.
- **Extensibility**: Easily plug in SNOMED/ICD ontologies, time-windowed aggregation, or external risk models.
- **Security**: For DHS or clinical usage, add PHI-sanitization, logging, and error handling modules.

This code serves as a **research-grade framework** for robust phenotyping and can be extended for federal or enterprise deployments.

Sources
