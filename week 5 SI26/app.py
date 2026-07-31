import os
import traceback
import torch
import gradio as gr
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# ============================================================
# Load Model
# ============================================================

MODEL_PATH = "best_model"   # Change if your folder name is different

processor = TrOCRProcessor.from_pretrained(MODEL_PATH)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_PATH)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# ============================================================
# Example Images
# ============================================================

EXAMPLE_DIR = "examples"

if os.path.exists(EXAMPLE_DIR):
    example_image_paths = [
        os.path.join(EXAMPLE_DIR, f)
        for f in os.listdir(EXAMPLE_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
else:
    example_image_paths = []

# ============================================================
# Prediction Function
# ============================================================

def predict(image):

    if image is None:
        return ""

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values.to(device)

    with torch.no_grad():

        generated_ids = model.generate(

            pixel_values,

            max_length=128,

            num_beams=4,

            early_stopping=True,

            no_repeat_ngram_size=2

        )

    prediction = processor.batch_decode(

        generated_ids,

        skip_special_tokens=True

    )[0]

    return prediction


# ============================================================
# Safe Prediction
# ============================================================

def predict_safe(image):

    if image is None:
        return "Please upload an image."

    try:
        return predict(image)

    except Exception:
        return traceback.format_exc()

# ============================================================
# Gradio Interface
# ============================================================

demo = gr.Interface(

    fn=predict_safe,

    inputs=gr.Image(type="pil", label="Upload Urdu Image"),

    outputs=gr.Textbox(
        label="Extracted Urdu Text",
        lines=8
    ),

    examples=example_image_paths if example_image_paths else None,

    title="Urdu OCR — Code Saviours SI-26",

    description="""
Upload an Urdu text image and click Submit.

The fine-tuned TrOCR model will recognize
the Urdu text and display it below.
"""
)

# ============================================================

if __name__ == "__main__":

    demo.launch()
     