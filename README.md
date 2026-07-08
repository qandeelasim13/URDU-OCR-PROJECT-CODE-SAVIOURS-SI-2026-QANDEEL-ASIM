# Urdu OCR Project — Code Saviours SI-26
### Code Saviours Summer Internship 2026 (SI-26)

**Author:** Qandeel Asim  
**Student ID:** 2023-BS-AI-037  
**Internship:** Code Saviours Summer Internship 2026 (SI-26)  
**Week:** 1 of 8  
**Project:** Urdu Optical Character Recognition (OCR)

---

# Project Overview

This repository contains the Week 1 implementation of an Urdu Optical Character Recognition (OCR) project. The primary objective of this phase is to build a high-quality labeled dataset that will later be used to train deep learning models for Urdu text recognition.

The notebook automates the complete dataset creation pipeline, including data collection, synthetic image generation, augmentation, labeling, validation, dataset splitting, and statistical analysis.

---

# Objectives

- Build a diverse Urdu OCR dataset.
- Collect images from multiple sources.
- Generate synthetic Urdu text images.
- Increase dataset diversity using augmentation.
- Store all labels in a single CSV file.
- Validate dataset quality.
- Create train and test datasets.
- Generate dataset statistics and visualizations.

---

# Dataset Sources

The dataset is created using **six different sources**.

| Source | Description |
|---------|-------------|
| **UTRSet-Real** | Public Urdu OCR research dataset containing printed Urdu text images. |
| **Synthetic Urdu Text** | Urdu sentences generated using the Noto Nastaliq Urdu font with Pillow. |
| **Augmented Images** | Automatically generated variations using blur, brightness adjustment, and rotation. |
| **Books** | Book-page style Urdu text images (synthetic or real). |
| **Signboards** | Urdu signboard-style images (synthetic or real). |
| **Newspaper** | Manual newspaper screenshots with OCR-generated transcription. |

---

# Workflow

The notebook performs the following steps:

1. Install required libraries.
2. Create project folder structure.
3. Download the public UTRSet dataset.
4. Generate synthetic Urdu text images.
5. Apply image augmentation.
6. Add book images.
7. Add signboard images.
8. Add newspaper screenshots.
9. Create and update `labels.csv`.
10. Validate all images and labels.
11. Split the dataset into training and testing sets.
12. Generate dataset statistics and visualizations.

---

# Folder Structure

```
URDU-OCR/
│
├── SI26_Week1_Qandeel.ipynb
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── utrset_real/
│   │   ├── synthetic/
│   │   ├── augmented/
│   │   ├── books/
│   │   ├── signboards/
│   │   └── newspaper/
│   │
│   ├── labels.csv
│   ├── train.csv
│   ├── test.csv
│   ├── dataset_stats.png
│   └── sample_grid.png
```

---

# Features

- Automated dataset creation
- Synthetic Urdu image generation
- Image augmentation
- Automatic dataset labeling
- Dataset validation
- Train/Test split
- Statistical analysis
- Sample image visualization

---

# Libraries Used

- Python 3
- Google Colab
- Pillow (PIL)
- OpenCV
- NumPy
- Pandas
- Matplotlib
- arabic-reshaper
- python-bidi
- EasyOCR
- gdown

---

# Output Files

| File | Description |
|------|-------------|
| `labels.csv` | Master dataset containing image path, label, source, and split. |
| `train.csv` | Training dataset. |
| `test.csv` | Testing dataset. |
| `dataset_stats.png` | Dataset statistics charts. |
| `sample_grid.png` | Random dataset image samples. |

---

# Dataset Validation

The notebook automatically checks:

- Missing images
- Corrupted files
- Empty labels
- Duplicate entries
- Invalid image paths

Only valid records are included in the final dataset.

---

# Train-Test Split

The validated dataset is divided into:

- **80% Training Data**
- **20% Testing Data**

This split is saved as:

- `train.csv`
- `test.csv`

---

# Visualizations

The notebook automatically generates:

- Images per source
- Text length distribution
- Dataset summary
- Random sample image grid

These visualizations help analyze dataset diversity and quality.

---

# Technologies

- Python
- Google Colab
- OCR Dataset Engineering
- Computer Vision
- Image Processing
- Data Augmentation
- Urdu NLP

---

# Future Work

The upcoming internship weeks will focus on:

- Image preprocessing
- OCR baseline evaluation
- Deep learning model development
- Model training
- Performance evaluation
- Deployment

---

# Author

**Qandeel Asim**

BS Artificial Intelligence

University of Faisalabad

Code Saviours Summer Internship 2026 (SI-26)

---

# License

This repository is intended for educational and research purposes as part of the Code Saviours Summer Internship 2026.
