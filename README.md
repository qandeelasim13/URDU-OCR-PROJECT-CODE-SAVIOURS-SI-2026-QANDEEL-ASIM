# Urdu OCR Project — Code Saviours SI-26

**Author:** Qandeel Asim
**Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Week:** 4 of 8 | **Project:** Urdu OCR Tool

---

## What Is This Project?

This is a complete Urdu OCR (Optical Character Recognition) system being built over 8 weeks.

- **Week 1** focused on collecting, organizing, and labeling a dataset of Urdu text images.
- **Week 2** focused on preprocessing that dataset and testing an existing off-the-shelf OCR engine (Tesseract) to identify its limitations on Urdu Nastaliq script — motivating the need for a custom-trained model.
- **Week 3** focused on expanding the dataset past the 200-image target, fixing data-quality issues found along the way, and building the PyTorch `Dataset` and `DataLoader` pipeline that fed the model this week.
- **Week 4** focused on fine-tuning a TrOCR-based model to actually read Urdu script, after discovering and fixing a fundamental vocabulary mismatch in the base pretrained model.

All collected images are stored under `data/raw/<category>/`, every image's ground-truth transcription is recorded in `data/labels.csv`, preprocessed images from Week 2 are stored under `data/processed/`, and the Week 4 fine-tuned model is stored under `models/trocr-urdu-finetuned/`.

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

## Week 3: Dataset Expansion + PyTorch Dataset Class & DataLoader

### Objective
This week focused on confirming the dataset has grown past the 200-image target, cleaning up data-quality issues discovered along the way, and building the PyTorch data pipeline (`Dataset` + `DataLoader`) that Week 4's model training ran on top of.

### What Was Done
1. Verified the dataset against the 200-image requirement by counting `labels.csv` directly — **248 images**, well past the target.
2. Discovered that 35 images (all from the `manual_screenshot` source) had a missing `split` value — they had never been assigned to `train` or `test`. Fixed this by assigning them 80/20 (`random_state=42` for reproducibility) and saving the correction back to `labels.csv`.
3. Discovered that some image paths recorded in `labels.csv` did not match their actual location on Google Drive (a side effect of earlier filename fixes). Built a path-resolution step that first tries the exact path, then falls back to a filename search across the whole project folder, so no image silently fails to load.
4. Implemented `UrduOCRDataset`, a custom PyTorch `Dataset` class that loads an image, converts it to RGB, runs it through the `TrOCRProcessor`, and tokenizes its Urdu label.
5. Tested the `Dataset` class end-to-end: correct tensor shapes, and a decode-and-compare check confirming a tokenized label decodes back to the exact original Urdu text.
6. Rebuilt the train/test split using the (now-corrected) `split` column — **198 training / 50 testing** samples.
7. Built `DataLoader` objects for both splits (`batch_size=8`, training shuffled, testing not shuffled) and confirmed batching works correctly.

### Week 3 Notebook Structure

| Section | Description |
|---|---|
| Step 0 — Setup | Mounts Google Drive, installs `transformers`/`torch`/`pillow`/`pandas` |
| Step 1 — Verify 200+ Images | Searches the project folder for `labels.csv`, counts total images, checks against the 200 target |
| Step 1 (composition check) | Breaks down image counts by `source` and `split` |
| Step 1c — Fix Missing Split Values | Detects rows with a missing `split` value and assigns them `train`/`test` (80/20), saving the fix back to `labels.csv` |
| Step 1b — Resolve Image Paths | Builds a filename index across the project folder and resolves every image's real path, dropping any that truly can't be found |
| Step 2 — Dataset Class | Defines and tests `UrduOCRDataset(Dataset)` |
| Step 3 — Train/Test Split | Rebuilds `train_dataset` / `test_dataset` using `torch.utils.data.Subset` and the corrected `split` column |
| Step 4 — DataLoader | Builds `train_loader` / `test_loader` and verifies a batch loads correctly |

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
- **PyTorch** (`torch.utils.data.Dataset`, `DataLoader`, `Subset`) — data pipeline
- **Hugging Face `transformers`** (`TrOCRProcessor`) — image + text preprocessing for the TrOCR model
- **pandas** — reading/fixing `labels.csv`
- **Pillow** — image loading
- **Google Colab** for compute and storage

### Submission
- Notebook: `SI26-Week3-qandeel.ipynb`
- Confirmation: *"My dataset has 248 images and loads correctly"*
- Updated `labels.csv` (248 entries, corrected `split` column) pushed to GitHub

---

## Week 4: Fine-Tuning TrOCR on the Urdu Dataset

### Objective
This week focused on fine-tuning Microsoft's TrOCR model — originally trained on English printed text — to read Urdu script, using the dataset and PyTorch pipeline built in Weeks 1–3.

### Key Finding: A Vocabulary Mismatch, Not a Bug
The stock `microsoft/trocr-base-printed` checkpoint uses an **English/Latin-only tokenizer (RoBERTa BPE)**. It has no representation for Urdu characters at all. Fine-tuning directly against it produced a training loss curve that looked healthy (steadily decreasing), but evaluation output was effectively garbage — Character Error Rate above 100% and a negative implied accuracy. This was traced back to a **vocabulary mismatch** between the pretrained tokenizer and the target language, not an error in the training code.

### The Fix
- Kept the **pretrained visual encoder** from TrOCR (frozen) — its ability to extract visual features from character images transfers regardless of language.
- Built a **character-level Urdu tokenizer** directly from the project's own dataset text, guaranteeing every character in the labels is representable.
- Attached a **new, smaller decoder** (trained from scratch) to the frozen encoder, sized for the Urdu character vocabulary.
- Verified the new tokenizer with a round-trip encode/decode test before training.

### What Was Done
1. Loaded the Week 3 dataset (`labels.csv`, 248 images, 198 train / 50 test) and resolved all image paths, including cases where images were nested one folder deeper than `labels.csv` recorded.
2. Loaded the pretrained `microsoft/trocr-base-printed` checkpoint and extracted its visual encoder.
3. Built a character-level Urdu tokenizer from the dataset's ground-truth text and confirmed it with a round-trip test.
4. Assembled a new `VisionEncoderDecoderModel` combining the frozen pretrained encoder with a freshly initialized decoder.
5. Trained the model using Hugging Face's `Seq2SeqTrainer` on Google Colab's GPU runtime, logging training loss every epoch.
6. Evaluated the fine-tuned model on the held-out test set using Character Error Rate (CER).
7. Spot-checked individual predictions against ground truth to confirm the model was producing genuine Urdu output rather than noise.
8. Plotted the training loss curve and saved the fine-tuned model back to Google Drive.

### Week 4 Notebook Structure

| Section | Description |
|---|---|
| Section 0 — Install | Installs `transformers`, `datasets`, `jiwer`, `evaluate`, `sentencepiece`, `accelerate` |
| Section 1 — GPU Check | Confirms a GPU runtime is active before training |
| Section 2 — Mount Drive | Mounts Google Drive |
| Section 3 — Load Dataset | Locates and loads `labels.csv`, rebuilds the train/test split |
| Section 4 — Resolve Image Paths | Drive-wide filename index so every image resolves regardless of nested folder differences |
| Section 5 — Load Pretrained TrOCR | Loads the pretrained checkpoint to reuse its visual encoder |
| Section 6 — Build Urdu-Capable Model | Builds the character-level Urdu tokenizer, freezes the pretrained encoder, attaches a fresh decoder |
| Section 7 — Dataset Class | Defines `UrduOCRDataset(Dataset)` using the new tokenizer |
| Section 8 — Build Datasets & Sanity Check | Builds `train_dataset`/`eval_dataset`, verifies tensor shapes |
| Section 9 — Training Setup & Training Loop | `Seq2SeqTrainingArguments`, CER-based `compute_metrics`, and `Seq2SeqTrainer.train()` |
| Section 10 — Evaluation | Computes final CER/accuracy on the test set, prints sample predictions vs. ground truth |
| Section 11 — Loss Curve | Plots and saves the training loss curve |
| Section 12 — Required Submission Statements | Prints final accuracy and training loss summary |
| Section 13 — Save Model | Saves the fine-tuned model and tokenizer vocabulary to Google Drive |

### Week 4 Results

```
My model accuracy is 38.53%
Training loss went from 2.9632 to 0.0046
Final CER on test set    : 0.6147
```

Sample predictions on the test set showed exact matches for shorter sentences, with more errors on longer, more complex sentences.

**Note on overfitting:** training loss dropped close to zero while test accuracy remained moderate, indicating the model overfit to the small training set (198 images) — a known and expected limitation given the dataset size at this stage of the project. This is flagged here rather than hidden, since understanding *why* a result looks the way it does is as important as the result itself.

### Tools Used (Week 4)
- **Hugging Face `transformers`** (`VisionEncoderDecoderModel`, `Seq2SeqTrainer`) — model architecture and training loop
- **Hugging Face `evaluate` + `jiwer`** — Character Error Rate computation
- **PyTorch** — custom tokenizer, dataset class, model assembly
- **Google Colab (GPU runtime)** — training compute
- **matplotlib** — training loss curve visualization

### Submission
- Notebook: `SI26-Week4-Qandeel.ipynb`
- Confirmation: *"My model accuracy is 38.53%"* / *"Training loss went from 2.9632 to 0.0046"*
- Loss curve screenshot and fine-tuned model pushed/saved alongside the notebook

---

## Week 4 Requirements

```bash
pip install transformers datasets jiwer evaluate sentencepiece accelerate
```

---

## Folder Structure

```
URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM/
│
├── SI26-Week1-Qandeel.ipynb     ← Week 1 notebook
├── SI26-Week2-Qandeel.ipynb     ← Week 2 notebook
├── SI26-Week3-qandeel.ipynb     ← Week 3 notebook
├── SI26-Week4-Qandeel.ipynb     ← Week 4 notebook
├── README.md                    ← This file
├── my_dataset_final.zip         ← Complete Week 1 dataset (zipped)
│
├── data/
│   ├── labels.csv                ← All labeled entries (image, text, source, split) — corrected in Week 3
│   ├── processed_labels.csv      ← Links raw image, processed image, text, source, split
│   ├── train.csv                 ← Training split (Week 1)
│   ├── test.csv                  ← Testing split (Week 1)
│   ├── gap_analysis.md           ← Week 2 gap analysis summary (auto-generated)
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
    └── trocr-urdu-finetuned/     ← Week 4: fine-tuned model + Urdu character tokenizer vocab
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
| PyTorch | `Dataset`/`DataLoader` data pipeline (Week 3), model assembly (Week 4) |
| Hugging Face `transformers` | `TrOCRProcessor` (Week 3), `VisionEncoderDecoderModel` + `Seq2SeqTrainer` (Week 4) |
| Hugging Face `evaluate` / `jiwer` | Character Error Rate computation (Week 4) |
| matplotlib | Dataset and results visualizations |

---

## Week-by-Week Plan

| Week | Task | Status |
|---|---|---|
| Week 1 | Dataset collection and labeling | ✅ Complete |
| Week 2 | Data preprocessing and OCR gap analysis | ✅ Complete |
| Week 3 | Dataset expansion, cleanup, and PyTorch Dataset/DataLoader pipeline | ✅ Complete |
| Week 4 | Fine-tuning TrOCR on the Urdu dataset | ✅ Complete |
| Week 5 | Deployment on Hugging Face Spaces | 🔜 Upcoming |

---

## Links
- **GitHub:** https://github.com/qandeelasim13/URDU-OCR-PROJECT-CODE-SAVIOURS-SI-2026-QANDEEL-ASIM
- **HuggingFace:** Coming in Week 5
