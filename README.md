# Urdu OCR Project — Code Saviours SI-26
**Author:** Qandeel Asim | **Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Week:** 2 of 8 | **Project:** Urdu OCR Tool

---

## What Is This Project?

This is a complete **Urdu OCR (Optical Character Recognition)** system being built
over 8 weeks. **Week 1** focused on collecting, organizing, and labeling a dataset
of Urdu text images. **Week 2** focused on preprocessing that dataset and testing
an existing off-the-shelf OCR engine (Tesseract) to identify its limitations on
Urdu Nastaliq script — motivating the need for a custom-trained model.

All collected images are stored under `data/raw/<category>/`, every image's
ground-truth transcription is recorded in `data/labels.csv`, and preprocessed
images from Week 2 are stored under `data/processed/`.

---

## Week 1: Dataset Collection & Labeling

### 1. Environment Setup
- Installed all required Python libraries: `Pillow`, `arabic-reshaper`, `python-bidi`, `gdown`, `matplotlib`, `easyocr`
- Set up Google Colab environment
- Created organized folder structure for dataset

### 2. Dataset Collection — 4 Sources

| Source | Type | Count | How |
|--------|------|-------|-----|
| UTRSet-Real | Real printed Urdu text | 60 images | Downloaded from Google Drive (ICDAR 2023 research dataset) |
| Synthetic Images | Generated Urdu text | 51 images | Rendered using Noto Nastaliq Urdu font with Pillow |
| Augmented Images | Modified synthetic images | 102 images | Blur, brightness, rotation applied automatically |
| Manual Screenshots | Real-world Urdu text | 33 images | Taken from Dawn Urdu, BBC Urdu, Jang, Wikipedia |
| **Total** | | **246 images** | |

### 3. Data Augmentation
Applied 3 types of augmentation on synthetic images to increase dataset size and variety:
- **Gaussian Blur** — simulates out-of-focus or low resolution scans
- **Brightness Jitter** — simulates different lighting conditions
- **Slight Rotation** — simulates tilted documents or camera angle

### 4. Dataset Labeling
- Every image paired with its correct Urdu text in `labels.csv`
- 4 columns: `image`, `text`, `source`, `split`
- Manual screenshots labeled using EasyOCR for automatic text extraction

### 5. Dataset Validation
- Checked every image: file exists, not blank/corrupt, label not empty
- Result: **246 valid entries, 0 invalid**

### 6. Train/Test Split
- 80% training set → `train.csv` (197 rows)
- 20% test set → `test.csv` (49 rows)

### 7. Visualizations
- Bar chart: images per source
- Histogram: text length distribution
- Sample grid: 12 random image previews

### Week 1 Notebook Structure

| Section | Description |
|---------|-------------|
| 0. Setup | Installs dependencies and imports all libraries |
| 1. Folder Structure | Creates `data/raw/<category>/` folders |
| 2. Helper Functions | `append_to_labels_csv()` and image quality validator |
| 3. Source 1 — UTRSet-Real | Downloads, extracts, and parses 60 real Urdu images |
| 4. Source 2 — Synthetic | Generates 51 Urdu text images using Noto Nastaliq font |
| 5. Source 3 — Augmentation | Creates 102 augmented variants (blur, brightness, rotation) |
| 6. Source 4 — Manual Screenshots | Adds 33 manually collected real-world Urdu images |
| 7. Dataset Validation | Checks all images for quality and completeness |
| 8. Train/Test Split | Splits dataset 80/20 into train.csv and test.csv |
| 9. Statistics & Visualizations | Bar chart, histogram, sample image grid |
| 10. Final Summary | Prints complete dataset breakdown |

### Dataset Sources

**UTRSet-Real**
- **What:** Real printed Urdu text word images from the UTRNet paper
- **Where:** Google Drive (auto-downloaded by notebook)
- **Citation:** Rahman, A., Ghosh, A., & Arora, C. (2023). *UTRNet: High-Resolution Urdu Text Recognition in Printed Documents.* ICDAR 2023, Springer Nature Switzerland.
- **License:** CC BY-NC-SA 4.0 (non-commercial, research use only)

**Synthetic Images**
- **What:** 51 Urdu sentences rendered as images
- **Font:** Noto Nastaliq Urdu (Google Fonts, OFL License)
- **Libraries:** `arabic_reshaper` + `python-bidi` for correct RTL rendering
- **Topics covered:** News, education, geography, technology, poetry, religion, signboards

**Manual Screenshots**
- **Sources:** [Dawn Urdu](https://urdu.dawn.com), [BBC Urdu](https://bbc.com/urdu), [Jang](https://jang.com.pk), [Urdu Wikipedia](https://ur.wikipedia.org)
- **Text extraction:** EasyOCR (Arabic + English model)

### Week 1 Output Files
```
data/labels.csv         ← 246 rows  (image, text, source, split)
data/train.csv          ← 197 rows  (80%)
data/test.csv           ←  49 rows  (20%)
data/dataset_stats.png  ← bar chart + histogram + pie chart
data/sample_grid.png    ← 12 random sample images
```

### Week 1 Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Images | 246 |
| Training Images | 197 (80%) |
| Test Images | 49 (20%) |
| Invalid/Corrupt Images | 0 |
| Unique Sources | 4 |
| UTRSet-Real | 60 images |
| Synthetic | 51 images |
| Augmented | 102 images |
| Manual Screenshots | 33 images |

### Terminal Output (Final Summary — Week 1)
```
==================================================
  URDU OCR DATASET — FINAL SUMMARY
==================================================
  Total labeled images : 246
  Training set         : 197
  Test set             :  49

  Breakdown by source:
    utrset_real              60
    synthetic                51
    augmented_blur           38
    augmented_brightness     35
    augmented_rotation       29
    manual_screenshot        33

  Output files:
    data/labels.csv
    data/train.csv
    data/test.csv
    data/dataset_stats.png
    data/sample_grid.png
==================================================
```

---

## Week 2: Image Preprocessing + Testing Existing OCR Tools

### Objective
This week focused on preparing the Week 1 Urdu image dataset for OCR, and testing
an existing off-the-shelf OCR engine (Tesseract) to identify its limitations on
Urdu Nastaliq script.

### What Was Done
- Built an image preprocessing pipeline: **grayscale → denoising → adaptive
  thresholding (binarization) → deskewing → resizing/normalization**.
- Applied this pipeline to all images from the Week 1 dataset and saved the
  output to `data/processed/`.
- Tested **Tesseract OCR** (`pytesseract`, `lang='urd'`) on both raw and
  preprocessed images, comparing outputs qualitatively.
- Documented the gap between Tesseract's performance and what is actually
  needed for reliable Urdu text recognition.

### Week 2 Notebook Structure

| Section | Description |
|---------|-------------|
| 1. Environment Setup | Installs Tesseract, Urdu language pack, OpenCV, pytesseract |
| 2. Imports | Loads all required libraries |
| 3. Mount Drive & Locate Dataset | Connects to Week 1 dataset in Google Drive |
| 4. Preprocessing Pipeline | Grayscale, denoise, binarize, deskew, resize functions |
| 5. Apply Pipeline & Save | Processes all images, saves to `data/processed/` |
| 6. Visualize Before/After | Shows sample raw vs. preprocessed image pairs |
| 7. Test Tesseract OCR | Runs Tesseract (`lang='urd'`) on raw and preprocessed samples |
| 8. Character Error Rate (CER) | Optional quantitative accuracy metric (if labels available) |
| 9. Gap Analysis | Documents why Tesseract fails on Urdu |
| 10. Auto-generate Gap Analysis | Writes `gap_analysis.md` summary file |
| 11. Push to GitHub | Commands to push processed data + notebook to repo |

### Tools Used (Week 2)
- OpenCV (Python) — image preprocessing
- Tesseract OCR + `tesseract-ocr-urd` language pack
- pytesseract — Python wrapper for Tesseract
- Google Colab + Google Drive for storage

### Tesseract Results Summary
Tesseract's Urdu output was frequently incomplete, garbled, or entirely incorrect
on Nastaliq-style text — even after preprocessing. Preprocessing improved image
contrast and reduced noise, but did not fix Tesseract's core inability to model
Nastaliq's diagonal, overlapping, context-dependent letterforms. Sample raw vs.
preprocessed outputs are included in `SI26-Week2-qandeel.ipynb`.

### Gap Analysis — Why Tesseract Fails on Urdu

1. **Cursive, context-dependent script** — Each Urdu Nastaliq letter's shape
   changes depending on its position (initial/medial/final/isolated) and its
   neighboring letters. Tesseract's model is mainly trained on Naskh-style text
   and struggles with Nastaliq's diagonal, overlapping strokes.
2. **Diagonal baseline and overlapping ligatures** — Nastaliq doesn't sit on a
   flat horizontal line; it flows diagonally and letters overlap, making
   character segmentation very difficult for a general-purpose engine.
3. **Limited, low-diversity training data** — Tesseract's Urdu model is trained
   on a small dataset and doesn't generalize well to different fonts,
   handwriting, or noisy/real-world images.
4. **Dot and diacritic confusion** — Many Urdu letters (e.g. ب، ت، ث، ن، ی) differ
   only by dot position/count, and are easily misclassified at lower resolutions.
5. **Inconsistent word-boundary spacing** — Tesseract's segmentation logic is
   built around Latin-script spacing rules, which don't reliably apply to
   Nastaliq text.

### Why This Project Matters
This gap is the core justification for building a **custom Urdu OCR model**
(e.g., a CNN/CRNN + CTC or Transformer-based architecture) trained specifically
on Nastaliq script data, rather than relying on general-purpose OCR engines like
Tesseract.

### Week 2 Requirements
```bash
apt-get install tesseract-ocr tesseract-ocr-urd
pip install pytesseract opencv-python-headless scikit-image pandas matplotlib
```

---

## Folder Structure

```
URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/
│
├── SI26-Week1-qandeel.ipynb     ← Week 1 notebook
├── SI26-Week2-qandeel.ipynb     ← Week 2 notebook
├── README.md                    ← This file
├── gap_analysis.md              ← Week 2 gap analysis summary
├── my_dataset_final.zip         ← Complete dataset (zipped)
│
└── data/
    ├── labels.csv               ← All 246 labeled entries
    ├── train.csv                ← 197 rows (80% split)
    ├── test.csv                 ←  49 rows (20% split)
    ├── dataset_stats.png        ← Statistics charts
    ├── sample_grid.png          ← Sample image preview
    │
    ├── raw/
    │   ├── newspaper/           ← 33 manual screenshots
    │   ├── synthetic/           ← 51 generated images
    │   ├── augmented/           ← 102 augmented images
    │   ├── other/               ← 60 UTRSet-Real images
    │   ├── books/
    │   └── signboards/
    │
    └── processed/                ← Week 2: preprocessed images
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Google Colab | Development environment |
| Python 3 | Programming language |
| Pillow | Image creation and augmentation |
| arabic-reshaper | Urdu character reshaping |
| python-bidi | Right-to-left text direction |
| gdown | Google Drive file download |
| EasyOCR | Automatic text extraction from images |
| OpenCV | Image preprocessing (Week 2) |
| Tesseract OCR | Existing OCR engine tested (Week 2) |
| matplotlib | Dataset visualizations |

---

## Week-by-Week Plan

| Week | Task | Status |
|------|------|--------|
| Week 1 | Dataset collection and labeling | ✅ Complete |
| Week 2 | Data preprocessing and OCR gap analysis | ✅ Complete |
| Week 3 | Model selection and fine-tuning setup | 🔜 Upcoming |
| Week 4 | Model training | 🔜 Upcoming |
| Week 5 | Deployment on Hugging Face Spaces | 🔜 Upcoming |

---

## Links
- **GitHub:** https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
- **HuggingFace:** Coming in Week 5
