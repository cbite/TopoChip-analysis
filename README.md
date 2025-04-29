# 📚 TopoChip Podocyte Image Analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15305938.svg)](https://doi.org/10.5281/zenodo.15305938)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cbite/TopoChip-analysis/main)


## Overview ##

This repository supports the paper:

**"Acquisition, Quality Control, and Architecture of a Large Image Dataset as a Tool for In Silico Cell Biological Research"**

It contains all code, metadata, SOPs, and reproducible workflows used to build a scalable, FAIR-aligned image analysis pipeline for studying how podocytes respond to biomaterial topographies using the TopoChip platform.

---

## 🔧 Repository Structure

```bash
TopoChip-analysis/
├── data/                 # Raw/processed data, metadata
│   └── metadata/         # TopoChip layout, imaging metadata, large archives
├── notebooks/            # Jupyter Notebooks: QC, segmentation, ML
├── scripts/              # MATLAB, Python, CellProfiler scripts
├── SOPs/                 # Experimental protocols (fabrication, imaging, etc.)
├── results/              # Figures and tables for publication
├── docs/                 # Manuscript and citation info
├── environment.yml       # Conda environment (recommended)
├── .gitattributes        # Git LFS config for large files
├── LICENSE               # Project license
└── README.md             # You're here