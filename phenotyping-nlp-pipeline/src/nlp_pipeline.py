#nlp_pipeline.py
# nlp_pipeline.py

import spacy
from spacy.tokens import Doc, Span, Token
from typing import List, Dict, Optional, Any
import logging

class NLPProcessor:
    """
    Clinical NLP Pipeline using spaCy for tokenization, sectioning, entity recognition, and contextualization.

    Designed for heterogeneous EHR free-text notes parsing with extensible clinical model integration.
    """

    def __init__(self, model_name: str = "en_core_sci_sm", disable: Optional[List[str]] = None):
        """
        Initializes the NLP pipeline.

        Args:
            model_name (str): SpaCy model name suited for clinical text (e.g., scispaCy).
            disable (Optional[List[str]]): Pipeline components to disable for optimization.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        disable = disable or []
        try:
            self.nlp = spacy.load(model_name, disable=disable)
            self.logger.info(f"Loaded spaCy model: {model_name}")
        except Exception as e:
            self.logger.error(f"Failed to load spaCy model '{model_name}': {e}")
            raise

        # Add custom pipeline components if needed, e.g., section segmenter
        self._add_section_segmenter()

    def _add_section_segmenter(self):
        """
        Adds custom section segmentation if not present.
        Basic rule-based implementation: splits on section header patterns.

        Extend/replace with machine-learned segmenter for production.
        """
        if "section_segmenter" not in self.nlp.pipe_names:
            self.nlp.add_pipe(self.section_segmenter, name="section_segmenter", last=True)
            self.logger.info("Added custom section segmenter to pipeline")

    def section_segmenter(self, doc: Doc) -> Doc:
        """
        Simple rule-based section segmentation based on common clinical note section headers.

        Marks sections in Doc._.sections as a list of dicts with 'title' and 'span'.

        Args:
            doc (Doc): spaCy Doc object

        Returns:
            Doc: spaCy Doc with sections annotated
        """
        import re
        sections = []
        section_start = 0
        pattern = re.compile(r'^(history of present illness|physical exam|assessment and plan|medications|impression|labs|diagnosis):?$', re.I)
        for i, token in enumerate(doc):
            if token.is_sent_start:
                sent_text = token.sent.text.strip().lower()
                if pattern.match(sent_text):
                    if sections:
                        # close previous section
                        sections[-1]['end'] = i - 1
                    sections.append({
                        'title': sent_text,
                        'start': i,
                        'end': None
                    })
        # Close last section
        if sections:
            sections[-1]['end'] = len(doc) - 1

        # Add as custom attribute (extension) to doc
        Doc.set_extension("sections", default=[], force=True)
        doc._.sections = sections
        return doc

    def process_text(self, text: str) -> Doc:
        """
        Process a single clinical note through the NLP pipeline.

        Args:
            text (str): Raw clinical note text.

        Returns:
            Doc: spaCy processed Doc.
        """
        if not text or not text.strip():
            self.logger.warning("Received empty text for processing.")
            return self.nlp("")

        doc = self.nlp(text)
        self.logger.info(f"Processed text - tokens: {len(doc)} sentences: {len(list(doc.sents))} sections: {len(doc._.sections) if hasattr(doc._, 'sections') else 0}")
        return doc

    def extract_entities(self, doc: Doc, labels: Optional[List[str]] = None) -> List[Span]:
        """
        Extracts entities optionally filtered by label(s).

        Args:
            doc (Doc): spaCy processed Doc.
            labels (Optional[List[str]]): List of entity labels to filter. If None, return all.

        Returns:
            List[Span]: List of spaCy Span entities.
        """
        entities = [ent for ent in doc.ents if labels is None or ent.label_ in labels]
        self.logger.info(f"Extracted {len(entities)} entities with labels filter: {labels}")
        return entities

    def extract_section_text(self, doc: Doc, section_title: str) -> Optional[str]:
        """
        Extracts raw text of specified section by title.

        Args:
            doc (Doc): spaCy processed Doc with sections.
            section_title (str): Target section title (case-insensitive).

        Returns:
            Optional[str]: Text of section or None if not found.
        """
        if not hasattr(doc._, "sections"):
            self.logger.warning("No sections found in doc.")
            return None
        for sec in doc._.sections:
            if sec['title'].lower() == section_title.lower():
                span = doc[sec['start']:sec['end'] + 1]
                return span.text
        self.logger.info(f"Section '{section_title}' not found.")
        return None

    # Extend for contextual cues or token section tagging here...

if __name__ == "__main__":
    # Example usage
    processor = NLPProcessor()
    sample_text = (
        "History of Present Illness:\n"
        "The patient reports fever and cough for 3 days.\n"
        "Physical Exam:\n"
        "Temp 101 F, lungs clear.\n"
        "Assessment and Plan:\n"
        "Likely viral infection, recommend supportive care."
    )
    doc = processor.process_text(sample_text)
    for sec in doc._.sections:
        print(f"Section: {sec['title']} | Text: {doc[sec['start']:sec['end']+1].text}")
