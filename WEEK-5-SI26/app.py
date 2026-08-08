import os
import streamlit as st
import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, TrOCRProcessor

MODEL_DIR = "qandeelasim13/urdu-ocr-trocr-si26"
MAX_LENGTH = 319
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "examples")
EXAMPLE_FILES = ['example_0.png', 'example_1.png', 'example_2.png', 'example_3.png']

st.set_page_config(page_title="Urdu OCR - Code Saviours SI-26", layout="centered")


@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = TrOCRProcessor.from_pretrained(MODEL_DIR)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_DIR).to(device)
    model.eval()
    return processor, model, device


processor, model, device = load_model()


@torch.no_grad()
def predict(image):
    if image is None:
        return ""
    image = image.convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
    generated_ids = model.generate(pixel_values, max_length=MAX_LENGTH, num_beams=4)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


st.title("Urdu OCR")
st.caption("Code Saviours SI-26 | Fine-tuned TrOCR (microsoft/trocr-base-printed)")
st.write(
    "Upload a photo or scan containing Urdu text. This tool fine-tunes the full "
    "pretrained TrOCR model on a custom Urdu dataset to read the text and return "
    "it as editable Unicode."
)
st.info(
    "Trained on a small dataset (~1,000 unique images) — works best on clean, "
    "printed, single-line Urdu text."
)

st.sidebar.header("Try an example")
selected_example = None
if EXAMPLE_FILES:
    choice = st.sidebar.radio(
        "One-click examples",
        options=["(none)"] + EXAMPLE_FILES,
    )
    if choice != "(none)":
        selected_example = os.path.join(EXAMPLES_DIR, choice)
        st.sidebar.image(selected_example, use_container_width=True)
else:
    st.sidebar.write("No example images bundled with this app.")

uploaded_file = st.file_uploader(
    "Upload an image containing Urdu text", type=["png", "jpg", "jpeg", "bmp", "webp"]
)

image_to_predict = None
if uploaded_file is not None:
    image_to_predict = Image.open(uploaded_file)
    st.image(image_to_predict, caption="Uploaded image", use_container_width=True)
elif selected_example is not None:
    image_to_predict = Image.open(selected_example)

if st.button("Extract Text", type="primary", disabled=image_to_predict is None):
    with st.spinner("Reading the image..."):
        try:
            result = predict(image_to_predict)
        except Exception as e:
            st.error(f"ERROR while predicting: {e}")
            result = None
    if result is not None:
        if not result.strip():
            st.warning("Model returned empty text for this image — try a clearer or higher-contrast image.")
        else:
            st.subheader("Extracted Urdu Text")
            st.markdown(
                f"<div style='direction: rtl; font-size: 1.4em; text-align: right;'>{result}</div>",
                unsafe_allow_html=True,
            )
elif image_to_predict is None:
    st.caption("Upload an image or pick an example from the sidebar, then click Extract Text.")
