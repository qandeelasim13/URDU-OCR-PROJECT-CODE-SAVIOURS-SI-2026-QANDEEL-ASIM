import gradio as gr
import traceback

def predict_safe(image):
    if image is None:
        return "No image received yet — upload one or pick an example above, then click Submit."
    try:
        result = predict(image)
    except Exception:
        return "ERROR while predicting:\n\n" + traceback.format_exc()

    if not result or not result.strip():
        return "[Model returned empty text for this image — try a clearer or higher-contrast image.]"

    return result


demo = gr.Interface(
    fn=predict_safe,
    inputs=gr.Image(type="pil", label="Upload an image containing Urdu text"),
    outputs=gr.Textbox(label="Extracted Urdu Text"),
    examples=example_image_paths if example_image_paths else None,
    title="Urdu OCR — Code Saviours SI-26",
    description=(
        "Upload a photo or scan containing Urdu text. This tool uses a TrOCR-style "
        "encoder-decoder model, fine-tuned on a custom Urdu dataset, to read the text "
        "and return it as editable Unicode. Pick one of the examples below for an "
        "instant one-click test."
    ),
)

demo.queue()
demo.launch(share=True, debug=True)
     