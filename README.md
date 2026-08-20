# Urdu OCR Project — Code Saviours SI-26

**Author:** Qandeel Asim
**Student ID:** 2023-BS-AI-037
**Internship:** Code Saviours Summer Internship 2026 (SI-26)
**Project:** Urdu OCR Tool | **Status:** ✅ Complete (5/5 weeks) — live and deployed

---

## Live Demo

**Try it here:** https://urdu-ocr-project-code-saviours-si-2026-appndeel-asim-n4vrzswoo.streamlit.app/


Upload a photo or scan of printed Urdu text and get back editable Unicode text — no installation needed.

Model weights: [huggingface.co/qandeelasim13/urdu-ocr-trocr-si26](https://huggingface.co/qandeelasim13/urdu-ocr-trocr-si26)

---

## What Is This Project?

A complete Urdu OCR (Optical Character Recognition) system, built over 5 weeks — from raw dataset collection through a fine-tuned deep learning model to a live, public web app.

- **Week 1** — collected and labeled a large-scale dataset of Urdu text images (scaled up from an initial small pilot to 3,160 images).
- **Week 2** — preprocessed that dataset, benchmarked an off-the-shelf OCR engine (Tesseract) to establish why a custom model was needed, and cleaned the dataset down to its final validated size.
- **Week 3** — verified the cleaned dataset, built a character-level Urdu tokenizer, and built the PyTorch `Dataset`/`DataLoader` pipeline.
- **Week 4** — fine-tuned a TrOCR-based model end-to-end to read Urdu script.
- **Week 5** — wrapped the fine-tuned model in a Streamlit web app and deployed it publicly.

All collected images are stored under `data/raw/<category>/`, every image's ground-truth transcription is recorded in `data/labels.csv`, preprocessed images from Week 2 are stored under `data/processed/`, and the final fine-tuned model is hosted on the Hugging Face Hub (see Live Demo above).

> **Note on dataset size across weeks:** the project started with a small 265-image pilot, then was rebuilt at scale in Week 1 (v2) to 3,160 images. Week 2's cleaning step removed 32 low-quality/duplicate rows (all from the `manual_screenshot` source), leaving **3,128 images** as the dataset used from Week 3 onward.

---

## Week 1 (v2): Large-Scale Dataset Collection & Labeling

### What Changed From the Original Pilot
The original Week 1 pass built 265 images from six sources using small hand-typed text lists (50 sentences, 8 paragraphs, 12 phrases) — not enough data or variety for the model to generalize on unseen images. Week 1 (v2) keeps the same six sources, folder structure, and CSV format, but replaces the hand-typed lists with a large pool of **real Urdu sentences pulled live from Urdu Wikipedia**, rendered with **three different Urdu fonts** instead of one.

### Environment Setup
- Installed: `Pillow`, `arabic-reshaper`, `python-bidi`, `gdown`, `matplotlib`, `easyocr`, `datasets`
- Google Colab environment, with a final step that syncs the whole `data/` folder to Google Drive for later weeks

### Dataset Collection — 6 Sources (Scaled)

| Source | What changed | Final count |
|---|---|---|
| UTRSet-Real | Samples raised 60 → 400 | **400** |
| Synthetic | 50 hardcoded sentences → real Wikipedia sentences, 3 fonts instead of 1 | **604** |
| Augmented — Blur | Applied to synthetic images | **618** |
| Augmented — Brightness | Applied to synthetic images | **598** |
| Augmented — Rotation | Applied to synthetic images | **596** |
| Books (synthetic paragraphs) | 8 hardcoded paragraphs → real Wikipedia paragraphs | **150** |
| Signboards (synthetic phrases) | 12 hardcoded phrases → real Wikipedia phrases + original 12 | **162** |
| Manual Screenshots | Unchanged — real headlines from Dawn Urdu, BBC Urdu, Jang, Wikipedia | **32** |
| **Total** | | **3,160 images** |

### Data Augmentation
Applied 3 augmented variants per synthetic image (raised from 2 in the original pilot):
- **Gaussian Blur** — simulates out-of-focus or low-resolution scans
- **Brightness Jitter** — simulates different lighting conditions
- **Slight Rotation** — simulates tilted documents or camera angle

### Dataset Labeling
- Every image is paired with its correct Urdu text in `labels.csv` (`image`, `text`, `source`, `split` columns)
- Manual screenshots labeled using EasyOCR for automatic text extraction, then manually verified

### Train/Test Split
- 80% training set → **2,528 rows**
- 20% test set → **632 rows**

### Week 1 (v2) — Final Summary

```
Total labeled images : 3,160
Training set          : 2,528
Test set               : 632

Breakdown by source:
augmented_blur           618
synthetic                604
augmented_brightness     598
augmented_rotation       596
utrset_real              400
signboards_synthetic     162
books_synthetic          150
manual_screenshot         32
```

### Dataset Sources — Details

**UTRSet-Real**
- Citation: Rahman, A., Ghosh, A., & Arora, C. (2023). *UTRNet: High-Resolution Urdu Text Recognition in Printed Documents*. ICDAR 2023, Springer Nature Switzerland.
- License: CC BY-NC-SA 4.0 (non-commercial, research use only)

**Synthetic Images**
- Real Urdu sentences pulled live from Urdu Wikipedia, rendered as images
- Fonts: three different Urdu fonts (incl. Noto Nastaliq Urdu, Google Fonts, OFL License)
- Libraries: `arabic_reshaper` + `python-bidi` for correct RTL rendering

**Manual Screenshots**
- Real Urdu news headlines and articles, screenshotted from Dawn Urdu, BBC Urdu, Jang, and Wikipedia

---

## Week 2 (v3): Preprocessing, Baseline OCR Test & Data Validation

### Objective
Preprocess the Week 1 (v2) images, benchmark Tesseract's out-of-the-box performance on Urdu, and clean/validate the dataset ahead of training.

### Part A — Preprocessing
- Built an Otsu-threshold + aspect-preserving resize pipeline and applied it across all raw images.
- Visually compared raw vs. processed images side by side, and checked dataset-wide raw image dimensions and processed black-pixel percentage as a QA pass.

### Part B — Baseline Tesseract Test
- Ran Tesseract (`lang='urd'`) on sample processed images and manually inspected the output against ground truth.
- Measured a **word-recovery rate**: on average, only **2.1%** of words across the 5 sampled images were correctly recovered by Tesseract — confirming, quantitatively, that an off-the-shelf engine is not viable for this script without a custom model.

**Example (raw Tesseract output vs. what it should read):**
```
Image: utrset_101 → Tesseract: "اسماباتن سے )گا کن سک اک سحا١‏ دتشبتی خ نی ررسدو" (mostly gibberish)
Image: utrset_255 → Tesseract: (blank)
Image: utrset_050 → Tesseract: (blank)
```

### Part C — Data Validation & Cleaning
1. Verified every image actually opens (no corrupt files).
2. Checked for empty, placeholder, or duplicate text labels — **removed 32 rows**, all from the `manual_screenshot` source.
3. Checked text length distribution per source.
4. Checked character vocabulary: **121 unique characters** across the dataset, including 50 non-Urdu-range characters (digits, punctuation — expected in small amounts).
5. Checked source balance and did a final visual spot-check (one image per source).
6. Saved the cleaned `labels.csv` back to Google Drive.

### Week 2 (v3) — Final Summary

```
Removed 32 rows (empty/placeholder/duplicate — all manual_screenshot)
Final dataset size : 3,128 images
Training set        : 2,502
Test set             : 626
```

### Tools Used (Week 2)
- **OpenCV (Python)** — Otsu thresholding and resizing
- **Tesseract OCR** + `tesseract-ocr-urd` language pack, **pytesseract**
- **Google Colab**

### Why Tesseract Fails on Urdu

1. **Cursive, context-dependent script** — each letter's shape changes with position and neighbors; Tesseract is mainly trained on Naskh-style text.
2. **Diagonal baseline and overlapping ligatures** — Nastaliq flows diagonally, breaking standard segmentation.
3. **Limited, low-diversity training data** — Tesseract's Urdu model doesn't generalize to real-world fonts/noise.
4. **Dot and diacritic confusion** — letters like ب، ت، ث، ن، ی differ only by dots, easily misclassified.
5. **Inconsistent word-boundary spacing** — segmentation logic built for Latin-script spacing rules.

### Why This Project Matters
A 2.1% word-recovery rate justified building a **custom Urdu OCR model** trained specifically on Nastaliq script data, rather than relying on general-purpose engines like Tesseract.

---

## Week 3 (v2): Dataset Verification + Tokenizer + PyTorch Dataset Class & DataLoader

### Objective
Confirm the cleaned dataset from Week 2 (v3) passed the training-readiness target, build a character-level Urdu tokenizer, and build the PyTorch data pipeline for training.

### What Was Done
1. Confirmed the dataset: **3,128 images**, well past the 1,000-image target for this stage.
2. Confirmed no missing `split` values (2,502 train / 626 test, matching Week 2).
3. Re-resolved every image path — **all 3,128 resolved successfully**, 0 missing.
4. Data-quality re-check: **0 corrupt/unreadable images, 0 empty text labels.**
5. Built a **character-level Urdu tokenizer** directly from the dataset's ground-truth text — **125-character vocabulary**, max label length 300 (longest actual label: 245 characters) — and verified it with a round-trip encode/decode test. Saved as `urdu_tokenizer_vocab.json` for Week 4.
6. Implemented `UrduOCRDataset`, a custom PyTorch `Dataset` that loads an image, converts to RGB, runs it through `TrOCRProcessor`, and tokenizes its Urdu label. Verified output tensor shapes: `pixel_values` → `[3, 384, 384]`, `labels` → `[300]`.
7. Rebuilt the train/test split (2,502 train / 626 test) and ran a **train/test leakage check**: 0 identical images appeared in both splits (382 identical *text* labels appeared in both — expected, since different images can share the same caption).
8. Built `DataLoader` objects (`batch_size=8`) — **313 training batches / 79 testing batches per epoch** — and confirmed batching works correctly.

### Week 3 (v2) — Final Summary

```
My dataset has 3,128 images and loads correctly
Training samples : 2,502
Testing samples   : 626
Urdu vocabulary size : 125 characters
Train/test image leakage : 0
```

### Tools Used (Week 3)
- **PyTorch** (`Dataset`, `DataLoader`) — data pipeline
- **Hugging Face `transformers`** (`TrOCRProcessor`) — image preprocessing
- **pandas**, **Pillow**, **Google Colab**

> **Note:** the character-level tokenizer built this week was used in an early Week 4 fine-tuning attempt. The final deployed model (Week 4 v8) instead reused TrOCR's own pretrained byte-level tokenizer — see Week 4 below for why.

---

## Week 4: Fine-Tuning TrOCR on the Urdu Dataset

### Objective
Fine-tune Microsoft's TrOCR model — originally trained on English printed text — to read Urdu script.

### Key Finding: A Vocabulary Mismatch, Not a Bug
The stock `microsoft/trocr-base-printed` checkpoint's tokenizer is a **byte-level BPE tokenizer** that can represent any Unicode text — including Urdu — via UTF-8 byte-level fallback tokens. An early attempt, using the Week 3 character-level Urdu tokenizer built from scratch, produced a healthy-looking loss curve but evaluated poorly, since it discarded the pretrained decoder entirely. The final architecture (**v8**) instead fine-tunes the **full pretrained model — encoder *and* decoder — end-to-end**, letting the model reuse everything it already knows about language modeling and only learn Urdu, rather than learning language modeling from zero.

### What Was Done
1. Loaded the dataset (3,160 rows in `labels.csv` from Week 1 — about 65% pre-augmented rotation/blur/brightness copies of **1,348 unique source images**).
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

This is below what a larger dataset would likely support — the notebook's own working estimate was 80–95% given more data. The main limiting factor is dataset size (~1,348 unique source images before augmentation). With more time or data, the next steps would be: growing the labeled dataset further, training for more epochs, and targeted data augmentation based on the worst-prediction error patterns.

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
| Week 1 | Large-scale dataset collection and labeling (3,160 images) | ✅ Complete |
| Week 2 | Preprocessing, Tesseract baseline test, and data cleaning (→ 3,128 images) | ✅ Complete |
| Week 3 | Dataset verification, tokenizer, and PyTorch Dataset/DataLoader pipeline | ✅ Complete |
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
├── SI26-Week1-Qandeel.ipynb     ← Week 1 (v2) notebook — large-scale dataset collection
├── SI26-Week2-Qandeel.ipynb     ← Week 2 (v3) notebook — preprocessing + Tesseract test + cleaning
├── SI26-Week3-qandeel.ipynb     ← Week 3 (v2) notebook — verification + tokenizer + DataLoader
├── SI26-Week4-Qandeel.ipynb     ← Week 4 notebook (model fine-tuning)
├── SI26-Week5-Qandeel.ipynb     ← Week 5 notebook (deployment)
├── README.md                    ← This file
├── my_dataset_final.zip         ← Complete dataset (zipped)
│
├── WEEK-5-SI26/                  ← Deployed Streamlit app
│   ├── app.py                    ← Streamlit app entry point
│   ├── requirements.txt          ← App dependencies (CPU-only torch)
│   └── examples/                 ← Sample images for one-click testing
│
├── data/
│   ├── labels.csv                ← All labeled entries (image, text, source, split)
│   ├── train.csv                 ← Training split (2,502 rows, post-cleaning)
│   ├── test.csv                  ← Testing split (626 rows, post-cleaning)
│   ├── urdu_tokenizer_vocab.json ← Character-level Urdu tokenizer (Week 3)
│   ├── dataset_stats.png         ← Week 1 statistics charts
│   ├── sample_grid.png           ← Week 1 sample image grid
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
- **Live App (Streamlit Community Cloud):** https://urdu-ocr-project-code-saviours-si-2026-appndeel-asim-n4vrzswoo.streamlit.app/

## Credit
Qandeel Asim
