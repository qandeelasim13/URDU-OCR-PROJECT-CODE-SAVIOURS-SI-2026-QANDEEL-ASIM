# Urdu OCR Project — Code Saviours SI-26

**Author:** Qandeel Asim
**Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Week:** 2 of 8 | **Project:** Urdu OCR Tool

---

## What Is This Project?

This is a complete Urdu OCR (Optical Character Recognition) system being built over 8 weeks.

- **Week 1** focused on collecting, organizing, and labeling a dataset of Urdu text images.
- **Week 2** focused on preprocessing that dataset and testing an existing off-the-shelf OCR engine (Tesseract) to identify its limitations on Urdu Nastaliq script — motivating the need for a custom-trained model.

All collected images are stored under `data/raw/<category>/`, every image's ground-truth transcription is recorded in `data/labels.csv`, and preprocessed images from Week 2 are stored under `data/processed/`.

---

## Week 1: Dataset Collection & Labeling

### Environment Setup
- Installed all required Python libraries: `Pillow`, `arabic-reshaper`, `python-bidi`, `gdown`, `matplotlib`, `easyocr`
- Set up Google Colab environment
- Created an organized folder structure for the dataset

### Dataset Collection — 6 Sources

| Source | Type | Count | How |
|---|---|---|---|
| UTRSet-Real | Real printed Urdu text | 60 images | Downloaded from Google Drive (ICDAR 2023 research dataset) |
| Synthetic Images | Generated Urdu text | 51 images | Rendered using Noto Nastaliq Urdu font with Pillow |
| Augmented — Blur | Modified synthetic images | 34 images | Gaussian blur applied automatically |
| Augmented — Brightness | Modified synthetic images | 34 images | Brightness jitter applied automatically |
| Augmented — Rotation | Modified synthetic images | 34 images | Slight rotation applied automatically |
| Manual Screenshots | Real-world Urdu text | 32 images | Taken from Dawn Urdu, BBC Urdu, Jang, Wikipedia |
| Synthetic Signboards | Generated short Urdu phrases | 12 images | Rendered signboard-style images with Pillow |
| Synthetic Book Pages | Generated Urdu paragraphs | 8 images | Rendered book-page-style images with Pillow |
| **Total** | | **265 images** | |

### Data Augmentation
Applied 3 types of augmentation on synthetic images to increase dataset size and variety:
- **Gaussian Blur** — simulates out-of-focus or low-resolution scans
- **Brightness Jitter** — simulates different lighting conditions
- **Slight Rotation** — simulates tilted documents or camera angle

### Dataset Labeling
- Every image is paired with its correct Urdu text in `labels.csv`
- 4 columns: `image`, `text`, `source`, `split`
- Manual screenshots labeled using EasyOCR for automatic text extraction, then manually verified

### Dataset Validation
- Checked every image: file exists, not blank/corrupt, label not empty
- Result: **265 valid entries, 0 invalid**

### Train/Test Split
- 80% training set → `train.csv` (**212 rows**)
- 20% test set → `test.csv` (**53 rows**)

### Visualizations
- Bar chart: images per source
- Histogram: text length distribution
- Sample grid: random image previews

### Dataset Sources — Details

**UTRSet-Real**
- What: Real printed Urdu text word images from the UTRNet paper
- Where: Google Drive (auto-downloaded by notebook)
- Citation: Rahman, A., Ghosh, A., & Arora, C. (2023). *UTRNet: High-Resolution Urdu Text Recognition in Printed Documents*. ICDAR 2023, Springer Nature Switzerland.
- License: CC BY-NC-SA 4.0 (non-commercial, research use only)

**Synthetic Images**
- What: 51 Urdu sentences rendered as images
- Font: Noto Nastaliq Urdu (Google Fonts, OFL License)
- Libraries: `arabic_reshaper` + `python-bidi` for correct RTL rendering
- Topics covered: news, education, geography, technology, poetry, religion, signboards

**Manual Screenshots**
- Real Urdu news headlines and articles, screenshotted directly from Dawn Urdu, BBC Urdu, Jang, and Wikipedia

### Urdu OCR Dataset — Final Summary

```
Total labeled images : 265
Training set         : 212
Test set              : 53

Breakdown by source:
utrset_real              60
synthetic                51
augmented_brightness     34
augmented_rotation       34
augmented_blur           34
manual_screenshot        32
signboards_synthetic     12
books_synthetic           8
```

---

## Week 2: Image Preprocessing + Testing Existing OCR Tools

### Objective
This week focused on preparing the Week 1 Urdu image dataset for OCR, and testing an existing off-the-shelf OCR engine (Tesseract) to identify its limitations on Urdu Nastaliq script.

### What Was Done
1. Loaded the Week 1 dataset directly from `data/labels.csv` + `data/raw/`, confirming all 265 image paths resolve correctly.
2. Verified and corrected the `train`/`test` split column, ensuring a reliable 80/20 split (212 train / 53 test) for future model training.
3. Built an image preprocessing pipeline: **grayscale → denoising → adaptive thresholding (binarization) → deskewing → resizing/normalization**.
4. Applied this pipeline to **all 265 images** from the Week 1 dataset (0 failures) and saved the output to `data/processed/`, mirroring Week 1's source subfolders.
5. Linked raw images, processed images, ground-truth text, source, and split together in `data/processed_labels.csv`.
6. Tested Tesseract OCR (`pytesseract`, `lang='urd'`) on both raw and preprocessed images, sampled across all sources.
7. Measured OCR accuracy quantitatively using **Character Error Rate (CER)**.
8. Manually reviewed the 5 worst-performing samples image-by-image to document exactly what went wrong.
9. Documented the gap between Tesseract's performance and what is actually needed for reliable Urdu text recognition.

### Week 2 Notebook Structure

| Section | Description |
|---|---|
| Step 0 — Load Week 1 Dataset | Loads `data/labels.csv` + `data/raw/` directly (or restores from `my_dataset_final.zip`) |
| Step 1 — Environment Setup | Installs Tesseract, Urdu language pack (`tesseract-ocr-urd`), OpenCV, pytesseract |
| Step 2 — Imports | Loads all required libraries |
| Step 3 — Read Labels & Confirm Link | Loads `labels.csv`, verifies every image path resolves, confirms counts match Week 1 |
| Step 3b — Fix Split Column | Recovers/regenerates a reliable 80/20 train/test split |
| Step 4 — Preprocessing Pipeline | Grayscale, denoise, binarize, deskew, resize functions |
| Step 5 — Apply Pipeline & Save | Processes all 265 images, saves to `data/processed/`, writes `data/processed_labels.csv` |
| Step 6 — Visualize Before/After | Shows sample raw vs. preprocessed image pairs |
| Step 7 — Test Tesseract OCR | Runs Tesseract (`lang='urd'`) on raw and preprocessed samples |
| Step 8 — Character Error Rate (CER) | Quantitative accuracy metric, overall and by source |
| Step 8b — Per-Image Gap Analysis | Manual breakdown of the 5 worst-performing images (actual text vs. Tesseract output vs. what went wrong) |
| Step 9 — Gap Analysis Reasons | Documents why Tesseract fails on Urdu |
| Step 10 — Auto-generate Gap Analysis | Writes `data/gap_analysis.md` summary file with live computed numbers |

### Tools Used (Week 2)
- **OpenCV (Python)** — image preprocessing
- **Tesseract OCR** + `tesseract-ocr-urd` language pack
- **pytesseract** — Python wrapper for Tesseract
- **Google Colab** for compute and storage

---

## Tesseract Results Summary

Tesseract's Urdu output was frequently incomplete, garbled, or entirely incorrect on Nastaliq-style text — both before and after preprocessing.

| Metric | Raw Images | Preprocessed Images |
|---|---|---|
| Average Character Error Rate (CER) | **84.8%** | **86.8%** |

**Preprocessing did not reduce the average CER overall** — CER actually rose slightly (by ~2 percentage points). Preprocessing helped on some sources (e.g. `augmented_blur`, where noise reduction genuinely cleaned up the image) but made results worse on others (e.g. `synthetic`), where binarization/deskewing distorted fine Nastaliq strokes Tesseract was already struggling to read.

This is an important finding: **cleaner-looking images do not automatically mean better OCR.** Preprocessing improved visual contrast and reduced noise, but it did not fix Tesseract's core inability to model Nastaliq's diagonal, overlapping, context-dependent letterforms — confirming that the bottleneck is the OCR engine itself, not image quality alone.

Sample raw vs. preprocessed outputs and per-source CER charts are included in `SI26-Week2-Qandeel.ipynb`.

---

## Why We Need a Better Model

### Per-Image Breakdown (5 Worst-Performing Samples)

> The table below is generated automatically by Step 8b of `SI26-Week2-Qandeel.ipynb`
> (`data/gap_analysis.md`). Run the notebook once and paste the live output here —
> the format is:

| # | Source | Actual Urdu Text | Tesseract Output | What Went Wrong |
|---|---|---|---|---|
| 1 | *(source)* | *(ground truth from labels.csv)* | *(Tesseract's actual output, or "empty" if blank)* | *(gibberish / missing words / wrong characters / dot confusion, etc.)* |
| 2 | *(source)* | ... | ... | ... |
| 3 | *(source)* | ... | ... | ... |
| 4 | *(source)* | ... | ... | ... |
| 5 | *(source)* | ... | ... | ... |

### Summary

**Tesseract fails on Urdu because** it was trained mainly on Naskh-style printed text, not the cursive, diagonally-flowing Nastaliq script most Urdu text actually uses. Nastaliq's overlapping ligatures and position-dependent letterforms break Tesseract's character segmentation, its Urdu language model is trained on limited, low-diversity data that does not generalize to real-world fonts and noise, and small dot/diacritic differences between otherwise identical letters are lost at normal image resolutions — together explaining the consistently high error rates measured above (84.8% CER on raw images, 86.8% on preprocessed images).

### Why Tesseract Fails on Urdu (General Reasons)

1. **Cursive, context-dependent script** — Each Urdu Nastaliq letter's shape changes depending on its position (initial/medial/final/isolated) and its neighboring letters. Tesseract's model is mainly trained on Naskh-style text and struggles with Nastaliq's diagonal, overlapping strokes.
2. **Diagonal baseline and overlapping ligatures** — Nastaliq doesn't sit on a flat horizontal line; it flows diagonally and letters overlap, making character segmentation very difficult for a general-purpose engine.
3. **Limited, low-diversity training data** — Tesseract's Urdu model is trained on a small dataset and doesn't generalize well to different fonts, handwriting, or noisy/real-world images.
4. **Dot and diacritic confusion** — Many Urdu letters (e.g. ب، ت، ث، ن، ی) differ only by dot position/count, and are easily misclassified at lower resolutions.
5. **Inconsistent word-boundary spacing** — Tesseract's segmentation logic is built around Latin-script spacing rules, which don't reliably apply to Nastaliq text.

### Why This Project Matters

This gap is the core justification for building a **custom Urdu OCR model** (e.g. a CNN/CRNN + CTC or Transformer-based architecture) trained specifically on Nastaliq script data, rather than relying on general-purpose OCR engines like Tesseract, or on preprocessing alone.

---

## Week 2 Requirements

```bash
apt-get install tesseract-ocr tesseract-ocr-urd
pip install pytesseract opencv-python-headless pandas matplotlib
```

---

## Folder Structure

```
URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/
│
├── SI26-Week1-Qandeel.ipynb     ← Week 1 notebook
├── SI26-Week2-Qandeel.ipynb     ← Week 2 notebook
├── README.md                    ← This file
├── my_dataset_final.zip         ← Complete Week 1 dataset (zipped)
│
└── data/
    ├── labels.csv                ← All 265 labeled entries (image, text, source, split)
    ├── processed_labels.csv      ← Links raw image, processed image, text, source, split
    ├── train.csv                 ← 212 rows (80% split)
    ├── test.csv                  ← 53 rows (20% split)
    ├── gap_analysis.md           ← Week 2 gap analysis summary (auto-generated)
    ├── dataset_stats.png         ← Week 1 statistics charts
    ├── before_after_grid.png     ← Week 2 raw vs. preprocessed samples
    ├── cer_by_source.png         ← Week 2 CER comparison chart
    │
    ├── raw/                      ← Week 1: original collected images
    │   ├── newspaper/            ← 32 manual screenshots
    │   ├── synthetic/            ← 51 generated images
    │   ├── augmented/            ← 102 augmented images (blur/brightness/rotation)
    │   ├── other/                ← 60 UTRSet-Real images
    │   ├── books/                ← 8 synthetic book-page images
    │   └── signboards/           ← 12 synthetic signboard images
    │
    └── processed/                ← Week 2: preprocessed images (mirrors raw/ structure)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Google Colab | Development environment |
| Python 3 | Programming language |
| Pillow | Image creation and augmentation |
| arabic-reshaper | Urdu character reshaping |
| python-bidi | Right-to-left text direction |
| gdown | Google Drive file download |
| EasyOCR | Automatic text extraction from images (Week 1 labeling) |
| OpenCV | Image preprocessing (Week 2) |
| Tesseract OCR | Existing OCR engine tested (Week 2) |
| pytesseract | Python wrapper for Tesseract (Week 2) |
| matplotlib | Dataset and results visualizations |

---

## Week-by-Week Plan

| Week | Task | Status |
|---|---|---|
| Week 1 | Dataset collection and labeling | ✅ Complete |
| Week 2 | Data preprocessing and OCR gap analysis | ✅ Complete |
| Week 3 | Model selection and fine-tuning setup | 🔜 Upcoming |
| Week 4 | Model training | 🔜 Upcoming |
| Week 5 | Deployment on Hugging Face Spaces | 🔜 Upcoming |

---

## Links

- **GitHub:** https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
- **HuggingFace:** Coming in Week 5
