# Urdu OCR Project — Code Saviours SI-26

**Author:** Qandeel Asim
**Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Project:** Urdu OCR Tool | **Status:** ✅ Complete (5/5 weeks) — live and deployed

---

## Live Demo

**Try it here:** [urdu-ocr-project-code-saviours-si-2026-appndeel-asim-9th9bhmrf.streamlit.app](https://urdu-ocr-project-code-saviours-si-2026-appndeel-asim-9th9bhmrf.streamlit.app/)

Upload a photo or scan of printed Urdu text and get back editable Unicode text — no installation needed.

Model weights: [huggingface.co/qandeelasim13/urdu-ocr-trocr-si26](https://huggingface.co/qandeelasim13/urdu-ocr-trocr-si26)

---

## What Is This Project?

A complete Urdu OCR (Optical Character Recognition) system, built over 5 weeks — from raw dataset collection through a fine-tuned deep learning model to a live, public web app.

- **Week 1** — collected, organized, and labeled a dataset of Urdu text images.
- **Week 2** — preprocessed that dataset and benchmarked an off-the-shelf OCR engine (Tesseract) to establish why a custom model was needed.
- **Week 3** — expanded the dataset, fixed data-quality issues, and built the PyTorch `Dataset`/`DataLoader` pipeline.
- **Week 4** — fine-tuned a TrOCR-based model end-to-end to read Urdu script.
- **Week 5** — wrapped the fine-tuned model in a Streamlit web app and deployed it publicly.

All collected images are stored under `data/raw/<category>/`, every image's ground-truth transcription is recorded in `data/labels.csv`, preprocessed images from Week 2 are stored under `data/processed/`, and the final fine-tuned model is hosted on the Hugging Face Hub (see Live Demo above).

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

### Urdu OCR Dataset — Week 1 Summary

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
Prepare the Week 1 Urdu image dataset for OCR, and test an off-the-shelf OCR engine (Tesseract) to identify its limitations on Urdu Nastaliq script.

### What Was Done
1. Loaded the Week 1 dataset directly from `data/labels.csv` + `data/raw/`, confirming all 265 image paths resolve correctly.
2. Verified and corrected the `train`/`test` split column (212 train / 53 test).
3. Built an image preprocessing pipeline: **grayscale → denoising → adaptive thresholding (binarization) → deskewing → resizing/normalization**.
4. Applied this pipeline to **all 265 images** (0 failures) and saved output to `data/processed/`.
5. Linked raw images, processed images, ground-truth text, source, and split in `data/processed_labels.csv`.
6. Tested Tesseract OCR (`pytesseract`, `lang='urd'`) on raw and preprocessed images, sampled across all sources.
7. Measured OCR accuracy using **Character Error Rate (CER)**.
8. Manually reviewed the 5 worst-performing samples image-by-image.
9. Documented the gap between Tesseract's performance and what reliable Urdu recognition actually needs.

### Week 2 Notebook Structure

| Section | Description |
|---|---|
| Step 0 — Load Week 1 Dataset | Loads `data/labels.csv` + `data/raw/` (or restores from `my_dataset_final.zip`) |
| Step 1 — Environment Setup | Installs Tesseract, Urdu language pack (`tesseract-ocr-urd`), OpenCV, pytesseract |
| Step 2 — Imports | Loads all required libraries |
| Step 3 — Read Labels & Confirm Link | Verifies every image path resolves, confirms counts match Week 1 |
| Step 3b — Fix Split Column | Recovers/regenerates a reliable 80/20 train/test split |
| Step 4 — Preprocessing Pipeline | Grayscale, denoise, binarize, deskew, resize functions |
| Step 5 — Apply Pipeline & Save | Processes all 265 images, saves to `data/processed/` |
| Step 6 — Visualize Before/After | Sample raw vs. preprocessed image pairs |
| Step 7 — Test Tesseract OCR | Runs Tesseract (`lang='urd'`) on raw and preprocessed samples |
| Step 8 — Character Error Rate (CER) | Quantitative accuracy metric, overall and by source |
| Step 8b — Per-Image Gap Analysis | Manual breakdown of the 5 worst-performing images |
| Step 9 — Gap Analysis Reasons | Documents why Tesseract fails on Urdu |
| Step 10 — Auto-generate Gap Analysis | Writes `data/gap_analysis.md` |

### Tools Used (Week 2)
- **OpenCV (Python)** — image preprocessing
- **Tesseract OCR** + `tesseract-ocr-urd` language pack
- **pytesseract** — Python wrapper for Tesseract
- **Google Colab** for compute and storage

### Tesseract Results Summary

| Metric | Raw Images | Preprocessed Images |
|---|---|---|
| Average Character Error Rate (CER) | **84.8%** | **86.8%** |

**Preprocessing did not reduce the average CER overall** — it rose slightly (~2 pp). Preprocessing helped some sources (e.g. `augmented_blur`) but hurt others (e.g. `synthetic`), where binarization/deskewing distorted fine Nastaliq strokes. **Cleaner-looking images don't automatically mean better OCR** — the bottleneck is Tesseract's model, not image quality alone.

### Why Tesseract Fails on Urdu

1. **Cursive, context-dependent script** — each letter's shape changes with position and neighbors; Tesseract is mainly trained on Naskh-style text.
2. **Diagonal baseline and overlapping ligatures** — Nastaliq flows diagonally, breaking standard segmentation.
3. **Limited, low-diversity training data** — Tesseract's Urdu model doesn't generalize to real-world fonts/noise.
4. **Dot and diacritic confusion** — letters like ب، ت، ث، ن، ی differ only by dots, easily misclassified.
5. **Inconsistent word-boundary spacing** — segmentation logic built for Latin-script spacing rules.

### Why This Project Matters
This gap justified building a **custom Urdu OCR model** trained specifically on Nastaliq script data, rather than relying on general-purpose engines like Tesseract.

---

## Week 3: Dataset Expansion + PyTorch Dataset Class & DataLoader

### Objective
Confirm the dataset passed the 200-image target, clean up data-quality issues, and build the PyTorch data pipeline (`Dataset` + `DataLoader`) for training.

### What Was Done
1. Verified the dataset against the 200-image requirement — **248 images**, past the target.
2. Fixed 35 `manual_screenshot` images missing a `split` value (assigned 80/20, `random_state=42`).
3. Built a path-resolution step for images whose recorded path didn't match their actual Drive location.
4. Implemented `UrduOCRDataset`, a custom PyTorch `Dataset` that loads an image, converts to RGB, runs it through `TrOCRProcessor`, and tokenizes its Urdu label.
5. Tested the `Dataset` class end-to-end (correct tensor shapes, decode round-trip check).
6. Rebuilt the train/test split — **198 training / 50 testing** samples.
7. Built `DataLoader` objects (`batch_size=8`, training shuffled, testing not) and confirmed batching.

### Week 3 Notebook Structure

| Section | Description |
|---|---|
| Step 0 — Setup | Mounts Drive, installs `transformers`/`torch`/`pillow`/`pandas` |
| Step 1 — Verify 200+ Images | Counts total images, checks against target |
| Step 1c — Fix Missing Split Values | Detects and fixes rows with a missing `split` value |
| Step 1b — Resolve Image Paths | Filename index across the project folder |
| Step 2 — Dataset Class | Defines and tests `UrduOCRDataset(Dataset)` |
| Step 3 — Train/Test Split | Rebuilds using `torch.utils.data.Subset` |
| Step 4 — DataLoader | Builds and verifies `train_loader`/`test_loader` |

### Week 3 Dataset Summary

```
Total labeled images       : 248
Training samples           : 198
Testing samples            : 50

Breakdown by source:
utrset_real              60
synthetic                51
manual_screenshot        35
augmented_blur           34
augmented_rotation       34
augmented_brightness     34
```

### Tools Used (Week 3)
- **PyTorch** (`Dataset`, `DataLoader`, `Subset`) — data pipeline
- **Hugging Face `transformers`** (`TrOCRProcessor`) — image + text preprocessing
- **pandas**, **Pillow**, **Google Colab**

---

## Week 4: Fine-Tuning TrOCR on the Urdu Dataset

### Objective
Fine-tune Microsoft's TrOCR model — originally trained on English printed text — to read Urdu script.

### Key Finding: A Vocabulary Mismatch, Not a Bug
The stock `microsoft/trocr-base-printed` checkpoint's tokenizer is a **byte-level BPE tokenizer** that can represent any Unicode text — including Urdu — via UTF-8 byte-level fallback tokens. An early attempt that assumed the tokenizer was English/Latin-only and built a custom character-level Urdu tokenizer from scratch trained a healthy-looking loss curve but evaluated poorly, since it discarded the pretrained decoder entirely. The final architecture (**v8**) instead fine-tunes the **full pretrained model — encoder *and* decoder — end-to-end**, letting the model reuse everything it already knows about language modeling and only learn Urdu, rather than learning language modeling from zero.

### What Was Done
1. Loaded and consolidated the labeled dataset — final version: **3,160 rows** in `labels.csv` (about 65% pre-augmented rotation/blur/brightness copies of **1,348 unique source images**), drawn from UTRSet-Real, synthetic Noto Nastaliq Urdu renders, augmented variants, and manual screenshots.
2. Built a **leakage-safe train/test split**, grouped by parent image, so augmented copies of the same source image never appear in both train and test.
3. Loaded the pretrained `microsoft/trocr-base-printed` checkpoint (encoder + decoder + `TrOCRProcessor` together).
4. Fine-tuned in **two phases**: a decoder-only warm-up, then the full model unfrozen at a lower learning rate — 15 epochs total.
5. Evaluated on the held-out test set using Character Error Rate (CER) and character-level accuracy.
6. Spot-checked individual predictions against ground truth.
7. Plotted the training loss curve and saved the fine-tuned model (`trocr-urdu-finetuned-v7` / v8 architecture) to Google Drive.

### Week 4 Results (Final — v8)

```
Character Error Rate (CER) on test set : 0.52
Character-level accuracy               : 47.66%
Training loss                          : 5.00 → 0.18 (avg per epoch, 15 epochs)
```

This is below what a larger dataset would likely support — the notebook's own working estimate was 80–95% given more data. The main limiting factor is dataset size (~1,000 unique source images before augmentation). With more time or data, the next steps would be: growing the labeled dataset further, training for more epochs, and targeted data augmentation based on the worst-prediction error patterns.

### Tools Used (Week 4)
- **Hugging Face `transformers`** (`VisionEncoderDecoderModel`, `Seq2SeqTrainer`, `TrOCRProcessor`)
- **Hugging Face `evaluate` + `jiwer`** — Character Error Rate computation
- **PyTorch**, **Google Colab (GPU runtime — Tesla T4)**, **matplotlib**

---

## Week 5: Web Application Deployment (Streamlit + Hugging Face Hub)

### Objective
Turn the Week 4 fine-tuned model into a live, public web app anyone can use to upload an Urdu image and get back extracted text — no installation, no account required.

### What Was Done
1. Loaded the fine-tuned model and `TrOCRProcessor` from the saved Week 4 v8 directory and switched to evaluation mode.
2. Built a **Streamlit** app (`app.py`) with an image upload widget, a set of one-click example images, and an "Extract Text" button that runs inference and displays the result as right-to-left formatted Urdu Unicode text.
3. Added error handling so invalid/empty uploads don't crash the app.
4. Uploaded the fine-tuned model weights and processor files (`config.json`, `model.safetensors`, tokenizer files, etc.) to a public **Hugging Face Hub model repository**, so the app loads the model directly by repo ID (`qandeelasim13/urdu-ocr-trocr-si26`) instead of bundling large weight files in GitHub.
5. Deployed the app on **Streamlit Community Cloud**, connected directly to the GitHub repository.
6. Worked through several real deployment issues along the way (kept here for anyone repeating this process):
   - A **space in the deployment folder name** broke Streamlit's dependency-file path resolution — fixed by renaming the folder to `WEEK-5-SI26` (no spaces).
   - The default Python version (3.14) was too new for `tokenizers`' prebuilt wheels, forcing a slow, failing Rust source build — fixed by explicitly setting **Python 3.11** in the app's Streamlit Cloud settings.
   - The default `torch` install pulled in the full **CUDA/GPU toolkit**, which is unnecessary (and memory-heavy) on Streamlit Cloud's CPU-only free tier, contributing to a "gone over resource limits" crash — mitigated by pointing `requirements.txt` at the CPU-only PyTorch wheel index (`--extra-index-url https://download.pytorch.org/whl/cpu`).
   - Bundled example images that were rendered with a font lacking Urdu glyph support showed up as placeholder boxes — flagged for regeneration with a proper Urdu-supporting font (e.g. Noto Nastaliq Urdu).
7. Verified the deployed app end-to-end: uploaded a real Urdu image, ran extraction, and confirmed readable Urdu output.

### Features
- Upload Urdu text images (PNG, JPG, BMP, WEBP) through a web interface, up to 200MB per file.
- Extract Urdu text using the fine-tuned TrOCR model, displayed as right-to-left Unicode.
- One-click example images for quick testing.
- Handles invalid uploads without crashing.
- Publicly accessible — no login required.

### Tools Used (Week 5)
- **Streamlit** — web app framework
- **Streamlit Community Cloud** — free public hosting
- **Hugging Face Hub** — model weight hosting (`qandeelasim13/urdu-ocr-trocr-si26`)
- **Hugging Face `transformers`** — model loading and inference
- **PyTorch** (CPU) — inference
- **Pillow (PIL)** — image handling
- **Google Colab** — development environment for the deployment notebook

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Google Colab | Development environment |
| Python 3.11 | Programming language (pinned for deployment) |
| Pillow | Image creation, augmentation, and handling |
| arabic-reshaper | Urdu character reshaping |
| python-bidi | Right-to-left text direction |
| gdown | Google Drive file download |
| EasyOCR | Automatic text extraction from images (Week 1 labeling) |
| OpenCV | Image preprocessing (Week 2) |
| Tesseract OCR + pytesseract | Existing OCR engine tested (Week 2) |
| PyTorch | `Dataset`/`DataLoader` pipeline, model fine-tuning, inference |
| Hugging Face `transformers` | `TrOCRProcessor`, `VisionEncoderDecoderModel`, `Seq2SeqTrainer` |
| Hugging Face `evaluate` / `jiwer` | Character Error Rate computation |
| Hugging Face Hub | Public model weight hosting |
| Streamlit | Web app framework |
| Streamlit Community Cloud | Public app hosting |
| matplotlib | Dataset and results visualizations |

---

## Week-by-Week Plan

| Week | Task | Status |
|---|---|---|
| Week 1 | Dataset collection and labeling | ✅ Complete |
| Week 2 | Data preprocessing and OCR gap analysis | ✅ Complete |
| Week 3 | Dataset expansion, cleanup, and PyTorch Dataset/DataLoader pipeline | ✅ Complete |
| Week 4 | Fine-tuning TrOCR on the Urdu dataset | ✅ Complete |
| Week 5 | Deployment as a live Streamlit web app | ✅ Complete |

---

## How to Run It Locally

```bash
git clone https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM.git
cd URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/WEEK-5-SI26
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`). The app downloads the fine-tuned model automatically from the Hugging Face Hub on first run.

---

## Folder Structure

```
URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/
│
├── SI26-Week1-Qandeel.ipynb     ← Week 1 notebook
├── SI26-Week2-Qandeel.ipynb     ← Week 2 notebook
├── SI26-Week3-qandeel.ipynb     ← Week 3 notebook
├── SI26-Week4-Qandeel.ipynb     ← Week 4 notebook (model fine-tuning)
├── SI26-Week5-Qandeel.ipynb     ← Week 5 notebook (deployment)
├── README.md                    ← This file
├── my_dataset_final.zip         ← Complete Week 1 dataset (zipped)
│
├── WEEK-5-SI26/                  ← Deployed Streamlit app
│   ├── app.py                    ← Streamlit app entry point
│   ├── requirements.txt          ← App dependencies (CPU-only torch)
│   └── examples/                 ← Sample images for one-click testing
│
├── data/
│   ├── labels.csv                ← All labeled entries (image, text, source, split)
│   ├── processed_labels.csv      ← Links raw image, processed image, text, source, split
│   ├── train.csv                 ← Training split (Week 1)
│   ├── test.csv                  ← Testing split (Week 1)
│   ├── gap_analysis.md           ← Week 2 gap analysis summary
│   ├── dataset_stats.png         ← Week 1 statistics charts
│   ├── before_after_grid.png     ← Week 2 raw vs. preprocessed samples
│   ├── cer_by_source.png         ← Week 2 CER comparison chart
│   ├── week4_training_loss.png   ← Week 4 training loss curve
│   │
│   ├── raw/                      ← Week 1: original collected images
│   │   ├── newspaper/            ← manual screenshots
│   │   ├── synthetic/            ← generated images
│   │   ├── augmented/            ← augmented images (blur/brightness/rotation)
│   │   ├── other/                ← UTRSet-Real images
│   │   ├── books/                ← synthetic book-page images
│   │   └── signboards/           ← synthetic signboard images
│   │
│   └── processed/                ← Week 2: preprocessed images (mirrors raw/ structure)
│
└── models/
    └── trocr-urdu-finetuned-v7/  ← Week 4: final fine-tuned model (also hosted on HF Hub)
```

---

## Links
- **GitHub:** https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
- **Hugging Face Model:** https://huggingface.co/qandeelasim13/urdu-ocr-trocr-si26
- **Live App (Streamlit Community Cloud):** https://urdu-ocr-project-code-saviours-si-2026-appndeel-asim-9th9bhmrf.streamlit.app/

## Credit
Qandeel Asim
Built during the Code Saviours ML/AI Internship — Batch SI-26.
