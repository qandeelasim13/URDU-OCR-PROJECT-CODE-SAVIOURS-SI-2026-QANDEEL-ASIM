# Urdu OCR Project — Code Saviours SI-26
**Author:** Qandeel Asim | **Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Week:** 1 of 8 | **Project:** Urdu OCR Tool

---

## What Is This Project?

This is **Week 1** of building a complete **Urdu OCR (Optical Character Recognition)** system.
The goal of Week 1 was to collect, organize, and label a dataset of Urdu text images that will be used to train an OCR model in Week 4.

This notebook builds a labeled image–text dataset by combining **four different data sources** into a single organized set, ready for training and evaluating an Urdu text recognition model.

All collected images are stored under `data/raw/<category>/` and every image's ground-truth transcription is recorded in `data/labels.csv`.

---

## What Was Done in Week 1

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

---

## Notebook Structure

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

---

## Folder Structure

```
URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/
│
├── SI26-Week1-qandeel.ipynb     ← Main notebook
├── README.md                    ← This file
├── my_dataset_final.zip         ← Complete dataset (zipped)
│
└── data/
    ├── labels.csv               ← All 246 labeled entries
    ├── train.csv                ← 197 rows (80% split)
    ├── test.csv                 ←  49 rows (20% split)
    ├── dataset_stats.png        ← Statistics charts
    ├── sample_grid.png          ← Sample image preview
    │
    └── raw/
        ├── newspaper/           ← 33 manual screenshots
        ├── synthetic/           ← 51 generated images
        ├── augmented/           ← 102 augmented images
        ├── other/               ← 60 UTRSet-Real images
        ├── books/
        └── signboards/
```

---

## Dataset Sources

### UTRSet-Real
- **What:** Real printed Urdu text word images from the UTRNet paper
- **Where:** Google Drive (auto-downloaded by notebook)
- **Citation:** Rahman, A., Ghosh, A., & Arora, C. (2023). *UTRNet: High-Resolution Urdu Text Recognition in Printed Documents.* ICDAR 2023, Springer Nature Switzerland.
- **License:** CC BY-NC-SA 4.0 (non-commercial, research use only)

### Synthetic Images
- **What:** 51 Urdu sentences rendered as images
- **Font:** Noto Nastaliq Urdu (Google Fonts, OFL License)
- **Libraries:** `arabic_reshaper` + `python-bidi` for correct RTL rendering
- **Topics covered:** News, education, geography, technology, poetry, religion, signboards

### Manual Screenshots
- **Sources:** [Dawn Urdu](https://urdu.dawn.com), [BBC Urdu](https://bbc.com/urdu), [Jang](https://jang.com.pk), [Urdu Wikipedia](https://ur.wikipedia.org)
- **Text extraction:** EasyOCR (Arabic + English model)

---

## Output

### Files Generated
```
data/labels.csv         ← 246 rows  (image, text, source, split)
data/train.csv          ← 197 rows  (80%)
data/test.csv           ←  49 rows  (20%)
data/dataset_stats.png  ← bar chart + histogram + pie chart
data/sample_grid.png    ← 12 random sample images
```

### Dataset Statistics

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

### Terminal Output (Final Summary)
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

## Requirements

```bash
pip install Pillow arabic-reshaper python-bidi gdown matplotlib easyocr
```

---

## How to Run

1. Open `SI26-Week1-qandeel.ipynb` in Google Colab
2. Click **Runtime → Run All**
3. For manual screenshots: upload images to `data/raw/newspaper/` via Colab file panel
4. Find all outputs in `data/` folder after run completes

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
| matplotlib | Dataset visualizations |

---

## Week-by-Week Plan

| Week | Task | Status |
|------|------|--------|
| Week 1 | Dataset collection and labeling | ✅ Complete |
| Week 2 | Data preprocessing and cleaning | 🔜 Next |
| Week 3 | Model selection and fine-tuning setup | 🔜 Upcoming |
| Week 4 | Model training | 🔜 Upcoming |
| Week 5 | Deployment on Hugging Face Spaces | 🔜 Upcoming |

---

## Links
- **GitHub:** https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
- **HuggingFace:** Coming in Week 5
- **Internship:** Code Saviours SI-26 | June 29 – August 29, 2026

