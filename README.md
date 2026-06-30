# URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
# SI'26 – Week 1: Urdu OCR Dataset Collection

**Author:** Qandeel Asim

## Overview

This notebook builds a small image–text dataset for Urdu Optical Character Recognition (OCR) by combining three different data sources into a single labeled set, ready to be used for training or evaluating an Urdu text recognition model.

All collected images are stored under `data/raw/<category>/`, and every image's ground-truth transcription is recorded in `data/labels.csv` with two columns: `image` (relative path) and `text` (the Urdu transcription).

## Data Sources

1. **UTRSet-Real** — a publicly available research dataset of real, printed Urdu text, released alongside the UTRNet paper (ICDAR 2023). The notebook downloads the dataset as a ZIP from Google Drive, extracts it, locates the ground-truth file (`gt.txt`), and copies a configurable number of samples (`N_SAMPLES`, default 60) into `data/raw/other/`.
2. **Synthetic Images** — a set of hand-written Urdu sentences rendered into images using the **Noto Nastaliq Urdu** font. `arabic_reshaper` reshapes the Urdu characters into their correctly joined forms, and `python-bidi` ensures proper right-to-left rendering. Images are saved to `data/raw/synthetic/`.
3. **Manual Screenshots** — Urdu text screenshots collected manually from sources such as Dawn Urdu, BBC Urdu, Jang, or Urdu Wikipedia, uploaded into `data/raw/newspaper/` (or `books/`, `signboards/`, `other/`) and labeled by hand.

## Notebook Structure

| Section | Description |
|---|---|
| 0. Setup | Installs dependencies (`Pillow`, `arabic-reshaper`, `python-bidi`, `gdown`) and imports |
| 1. Folder Structure | Creates the `data/raw/<category>/` folders |
| 2. Helper Function | `append_to_labels_csv()` safely merges new rows into `labels.csv` without overwriting or duplicating existing entries |
| 3. Source 1 | Downloads, extracts, and parses UTRSet-Real samples |
| 4. Source 2 | Generates synthetic Urdu text images |
| 5. Source 3 | Placeholder cell for manually uploaded screenshots and their transcriptions |
| 6. Final Check | Prints the total number of labeled entries and a preview of the dataset |

## Requirements

- Python 3
- `Pillow`, `arabic-reshaper`, `python-bidi`, `gdown`

These are installed automatically by the first cell of the notebook:

```bash
pip install Pillow arabic-reshaper python-bidi gdown
```

## How to Run

1. Open the notebook in Google Colab (or a local Jupyter environment).
2. Run all cells in order from top to bottom.
3. For **Source 3 (Manual Screenshots)**: upload your screenshots into the relevant `data/raw/<category>/` folder via the Colab file panel, then fill in the `manual_rows` list with each image's path and its correct Urdu transcription before running that cell.
4. After running, check `data/labels.csv` for the complete set of labeled image–text pairs.

## Output

```
data/
├── labels.csv
└── raw/
    ├── newspaper/
    ├── books/
    ├── signboards/
    ├── synthetic/
    └── other/
```

## Dataset Citation

> Rahman, A., Ghosh, A., & Arora, C. (2023). *UTRNet: High-Resolution Urdu Text Recognition in Printed Documents.* Proceedings of ICDAR 2023, Springer Nature Switzerland.

**License:** UTRSet-Real is distributed under CC BY-NC-SA 4.0 (non-commercial, research use only). Synthetic and manually collected images in this repository follow the same non-commercial, research-use restriction.
