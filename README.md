# Probabilistic Phenotyping NLP Pipeline (Department of Homeland Security Project)

This repository showcases an end-to-end clinical Natural Language Processing (NLP) pipeline developed to support **probabilistic phenotyping** from **heterogeneous Electronic Health Record (EHR) data**, as part of a research contract with the **U.S. Department of Homeland Security (DHS)**.

## 🔬 Project Overview

This pipeline ingests clinical data—including **free-text notes**, **medications**, **diagnosis codes**, and **laboratory results**—and produces **phenotype representations** by combining:

- Advanced NLP (via `spaCy`)
- Valence detection
- Structured token extraction
- Probabilistic modeling
- Domain-informed phenotyping

Inspired by the UPhenome model [Pivovarov et al., 2015](https://doi.org/10.1016/j.jbi.2015.10.001), this system facilitates **data harmonization**, **phenotype discovery**, and **cohort extraction**.

## 📊 System Architecture

![Architecture Diagram](docs/architecture-overview.png)

Core components include:

- `DbReader`: Reads raw EHR text files
- `spaCy NLP`: Tokenizes, sections, and contextualizes input
- `Valence Detector`: Labels n-gram positivity/negativity
- `Phenotyping Engine`: Tags tokens into clinically-related groups
- `DbWriter`: Outputs structured phenotype summaries

## 🧪 Use Case

This tool enables federal agencies to rapidly classify large volumes of patient data using NLP-powered phenotyping for:

- Public health threat detection
- Syndromic surveillance
- Clinical research and risk stratification
- Emergency response analytics

## 📁 Directory Structure

| Folder | Description |
|--------|-------------|
| `src/` | Core pipeline modules |
| `docs/` | Diagrams and publications |
| `notebooks/` | Jupyter walkthroughs |
| `data/` | Sample input EHR files |
| `requirements.txt` | Python dependencies |

## 🧠 Research Foundation

This work builds upon:
- [Learning Probabilistic Phenotypes from Heterogeneous EHR Data](https://doi.org/10.1016/j.jbi.2015.10.001) :contentReference[oaicite:0]{index=0}
- spaCy-based document parsing and token pipelines
- Clinical informatics practices used in syndromic surveillance by DHS

## 🔐 Acknowledgments

Developed under federal contract for the **Department of Homeland Security**. Portions of the model design and methodology are derived from academic work by **Columbia University Biomedical Informatics**.

## 📜 License

[MIT License](LICENSE)
